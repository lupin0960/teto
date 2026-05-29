import asyncio
from typing import Any, Callable, Dict, Optional

import aiohttp

from .ribbon import Ribbon


class Bot:
    """
    Event-driven TETR.IO bot framework.

    Usage::

        bot = Bot(token="YOUR_TOKEN")

        @bot.event
        async def on_ready(user):
            print(f"Logged in as {user['username']}")

        @bot.event
        async def on_chat(msg):
            print(msg)

        bot.run()
    """

    _RIBBON_ENDPOINT_URL = "https://tetr.io/api/server/ribbon"
    _ENV_URL = "https://tetr.io/api/server/environment"

    def __init__(self, token: str):
        self._token = token
        self._handlers: Dict[str, Callable] = {}
        self._ribbon: Optional[Ribbon] = None
        self.user: Optional[Dict[str, Any]] = None  # set after authorize

    # ------------------------------------------------------------------
    # Decorator
    # ------------------------------------------------------------------

    def event(self, func: Callable) -> Callable:
        """
        Register an event handler.

        The function name must be ``on_<event>``, e.g. ``on_ready``,
        ``on_chat``, ``on_social_dm``.
        """
        if not func.__name__.startswith("on_"):
            raise ValueError(f"Event handler name must start with 'on_': {func.__name__}")
        event_name = func.__name__[3:]  # strip 'on_'
        self._handlers[event_name] = func
        return func

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Start the bot (blocking)."""
        asyncio.run(self._start())

    async def start(self) -> None:
        """Async entry point for use inside an existing event loop."""
        await self._start()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    async def _start(self) -> None:
        async with aiohttp.ClientSession() as session:
            endpoint, signature = await self._fetch_connection_info(session)

        self._ribbon = Ribbon(on_message=self._dispatch_raw)
        await self._ribbon.connect(endpoint)
        await self._ribbon.send("new")

        # hello → authorize is handled inside _dispatch_raw
        self._signature = signature
        await self._ribbon.listen()

    async def _fetch_connection_info(self, session: aiohttp.ClientSession):
        """Fetch the recommended worker endpoint and latest signature from TETR.IO."""
        headers = {"Authorization": f"Bearer {self._token}"}

        async with session.get(self._RIBBON_ENDPOINT_URL, headers=headers) as resp:
            data = await resp.json()
            endpoint = data.get("endpoint", "wss://tetr.io/ribbon")

        async with session.get(self._ENV_URL) as resp:
            env = await resp.json()
            signature = {
                "commit": env.get("commit", {"id": "unknown"})
            }

        return endpoint, signature

    def _dispatch_raw(self, msg: Dict[str, Any]) -> None:
        """Called for every decoded Ribbon message."""
        command = msg.get("command")
        if command is None:
            return

        # Built-in protocol handling
        if command == "hello":
            asyncio.create_task(self._handle_hello(msg))
            return
        if command == "authorize":
            asyncio.create_task(self._handle_authorize(msg))
            return
        if command == "migrate":
            asyncio.create_task(self._handle_migrate(msg))
            return
        if command == "Buffer":
            # Server requests we buffer; re-dispatch buffered messages
            for buffered in msg.get("data", {}).get("packets", []):
                self._dispatch_raw(buffered)
            return

        # Map Ribbon command → on_<event> handler
        # e.g. "chat" → on_chat, "social.dm" → on_social_dm
        event_name = command.replace(".", "_")
        handler = self._handlers.get(event_name)
        if handler:
            asyncio.create_task(handler(msg.get("data", msg)))

    async def _handle_hello(self, msg: Dict[str, Any]) -> None:
        """Respond to server hello with authorize."""
        await self._ribbon.send("authorize", {
            "token": self._token,
            "handling": {
                "arr": 0, "das": 0, "dcd": 0, "sdf": 5,
                "safelock": False, "cancel": False
            },
            "signature": self._signature,
        })

    async def _handle_authorize(self, msg: Dict[str, Any]) -> None:
        """Handle server authorize response."""
        data = msg.get("data", {})
        if not data.get("success", False):
            reason = data.get("reason", "unknown")
            raise RuntimeError(f"Authorization failed: {reason}")

        self.user = data.get("worker", {}).get("user")
        handler = self._handlers.get("ready")
        if handler:
            await handler(self.user)

    async def _handle_migrate(self, msg: Dict[str, Any]) -> None:
        """Reconnect to a new Ribbon worker endpoint."""
        new_endpoint = msg.get("data", {}).get("endpoint")
        if not new_endpoint:
            return
        await self._ribbon.close()
        self._ribbon = Ribbon(on_message=self._dispatch_raw)
        await self._ribbon.connect(new_endpoint)
        await self._ribbon.send("new")
        await self._ribbon.send("resume", {"sessionid": self._session_id})
        await self._ribbon.listen()

    # ------------------------------------------------------------------
    # Actions (call from event handlers)
    # ------------------------------------------------------------------

    async def send_chat(self, content: str) -> None:
        await self._ribbon.send("chat", {"content": content})

    async def create_room(self, room_type: str = "private") -> None:
        """room_type: 'public' or 'private'"""
        await self._ribbon.send("createroom", {"type": room_type})

    async def join_room(self, room_id: str) -> None:
        await self._ribbon.send("joinroom", {"id": room_id})

    async def leave_room(self) -> None:
        await self._ribbon.send("leaveroom", {})

    async def send_dm(self, recipient_id: str, content: str) -> None:
        await self._ribbon.send("social.dm", {
            "recipient": recipient_id,
            "msg": {"content": content, "content_safe": content}
        })

    async def close(self) -> None:
        if self._ribbon:
            await self._ribbon.close()
