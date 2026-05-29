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

        bot.run()
    """

    _RIBBON_ENDPOINT_URL = "https://tetr.io/api/server/ribbon"
    _ENV_URL = "https://tetr.io/api/server/environment"

    def __init__(self, token: str):
        self._token = token
        self._handlers: Dict[str, Callable] = {}
        self._ribbon: Optional[Ribbon] = None
        self._session: Optional[aiohttp.ClientSession] = None
        self._signature: Dict[str, Any] = {"commit": {"id": "unknown"}}
        self.user: Optional[Dict[str, Any]] = None

    def event(self, func: Callable) -> Callable:
        if not func.__name__.startswith("on_"):
            raise ValueError(f"Event handler name must start with 'on_': {func.__name__}")
        event_name = func.__name__[3:]
        self._handlers[event_name] = func
        return func

    def run(self) -> None:
        asyncio.run(self._start())

    async def start(self) -> None:
        await self._start()

    async def _start(self) -> None:
        self._session = aiohttp.ClientSession()
        try:
            endpoint, self._signature = await self._fetch_connection_info()
            print(f"[teto] Connecting to: {endpoint}")

            self._ribbon = Ribbon(session=self._session, on_message=self._dispatch_raw)
            await self._ribbon.connect(endpoint)
            await self._ribbon.send("new")
            await self._ribbon.listen()
        finally:
            await self._session.close()

    async def _fetch_connection_info(self):
        headers = {"Authorization": f"Bearer {self._token}"}

        async with self._session.get(self._RIBBON_ENDPOINT_URL, headers=headers) as resp:
            data = await resp.json(content_type=None)
            print(f"[teto] ribbon endpoint response: {data}")
            endpoint = data.get("endpoint", "wss://tetr.io/ribbon")

        async with self._session.get(self._ENV_URL) as resp:
            env = await resp.json(content_type=None)
            signature = {"commit": env.get("commit", {"id": "unknown"})}

        return endpoint, signature

    def _dispatch_raw(self, msg: Dict[str, Any]) -> None:
        command = msg.get("command")
        if command is None:
            return

        print(f"[teto] recv: {command}")

        if command == "hello":
            asyncio.create_task(self._handle_hello())
            return
        if command == "authorize":
            asyncio.create_task(self._handle_authorize(msg))
            return
        if command == "migrate":
            asyncio.create_task(self._handle_migrate(msg))
            return
        if command == "Buffer":
            for buffered in msg.get("data", {}).get("packets", []):
                self._dispatch_raw(buffered)
            return

        event_name = command.replace(".", "_")
        handler = self._handlers.get(event_name)
        if handler:
            asyncio.create_task(handler(msg.get("data", msg)))

    async def _handle_hello(self) -> None:
        await self._ribbon.send("authorize", {
            "token": self._token,
            "handling": {
                "arr": 0, "das": 0, "dcd": 0, "sdf": 5,
                "safelock": False, "cancel": False
            },
            "signature": self._signature,
        })

    async def _handle_authorize(self, msg: Dict[str, Any]) -> None:
        data = msg.get("data", {})
        print(f"[teto] authorize response: {data}")
        if not data.get("success", False):
            reason = data.get("reason", "unknown")
            raise RuntimeError(f"Authorization failed: {reason}")

        self.user = data.get("worker", {}).get("user")
        handler = self._handlers.get("ready")
        if handler:
            await handler(self.user)

    async def _handle_migrate(self, msg: Dict[str, Any]) -> None:
        new_endpoint = msg.get("data", {}).get("endpoint")
        if not new_endpoint:
            return
        await self._ribbon.close()
        self._ribbon = Ribbon(session=self._session, on_message=self._dispatch_raw)
        await self._ribbon.connect(new_endpoint)
        await self._ribbon.send("new")
        await self._ribbon.listen()

    async def send_chat(self, content: str) -> None:
        await self._ribbon.send("chat", {"content": content})

    async def create_room(self, room_type: str = "private") -> None:
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
