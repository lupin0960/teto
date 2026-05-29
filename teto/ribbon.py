import asyncio
import struct
from typing import Any, Callable, Dict, Optional

import aiohttp
import msgpack


class Ribbon:
    """
    TETR.IO Ribbon WebSocket connection.
    Handles packet encoding/decoding (0x45, 0xAE, 0x58, 0xB0),
    message ordering, and ping keepalive.

    Ribbon.md: https://github.com/lemoncove/tetrio-bot-docs/blob/main/Ribbon.md
    """

    PING_INTERVAL = 5.0  # seconds
    GENERIC_ENDPOINT = "wss://tetr.io/ribbon"

    def __init__(self, on_message: Callable[[Dict[str, Any]], None]):
        self._on_message = on_message
        self._ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self._session: Optional[aiohttp.ClientSession] = None
        self._send_id = 0
        self._ping_task: Optional[asyncio.Task] = None

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    async def connect(self, endpoint: str) -> None:
        self._session = aiohttp.ClientSession()
        self._ws = await self._session.ws_connect(endpoint)
        self._ping_task = asyncio.create_task(self._ping_loop())

    async def send(self, command: str, data: Optional[Dict[str, Any]] = None) -> None:
        self._send_id += 1
        msg: Dict[str, Any] = {"id": self._send_id, "command": command}
        if data is not None:
            msg["data"] = data
        packet = b"\x45" + msgpack.packb(msg, use_bin_type=True)
        await self._ws.send_bytes(packet)

    async def listen(self) -> None:
        """Receive loop — call this in a task or directly await it."""
        async for ws_msg in self._ws:
            if ws_msg.type == aiohttp.WSMsgType.BINARY:
                for msg in self._decode_packet(ws_msg.data):
                    self._on_message(msg)
            elif ws_msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                break

    async def close(self) -> None:
        if self._ping_task:
            self._ping_task.cancel()
        if self._ws and not self._ws.closed:
            await self.send("die")
            await self._ws.close()
        if self._session:
            await self._session.close()

    # ------------------------------------------------------------------
    # Packet decoding
    # ------------------------------------------------------------------

    def _decode_packet(self, data: bytes) -> list:
        """Parse a raw WebSocket binary frame into a list of message dicts."""
        if not data:
            return []

        header = data[0]

        if header == 0x45:  # standard
            return [msgpack.unpackb(data[1:], raw=False)]

        if header == 0xAE:  # extracted id
            extracted_id = struct.unpack_from(">I", data, 1)[0]
            msg = msgpack.unpackb(data[5:], raw=False)
            msg["id"] = extracted_id
            return [msg]

        if header == 0x58:  # batch
            return self._decode_batch(data[1:])

        if header == 0xB0:  # extension (ping/pong)
            # 0x0C = pong from server; nothing to dispatch
            return []

        return []

    def _decode_batch(self, data: bytes) -> list:
        lengths = []
        offset = 0
        while True:
            length = struct.unpack_from(">I", data, offset)[0]
            offset += 4
            if length == 0:
                break
            lengths.append(length)

        messages = []
        for length in lengths:
            chunk = data[offset: offset + length]
            offset += length
            messages.extend(self._decode_packet(chunk))
        return messages

    # ------------------------------------------------------------------
    # Ping keepalive
    # ------------------------------------------------------------------

    async def _ping_loop(self) -> None:
        try:
            while True:
                await asyncio.sleep(self.PING_INTERVAL)
                if self._ws and not self._ws.closed:
                    await self._ws.send_bytes(b"\xb0\x0b")
        except asyncio.CancelledError:
            pass
