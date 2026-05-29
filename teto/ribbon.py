import asyncio
import struct
from typing import Any, Callable, Dict, Optional

import aiohttp
import msgpack


class Ribbon:
    PING_INTERVAL = 5.0

    def __init__(self, session: aiohttp.ClientSession, on_message: Callable[[Dict[str, Any]], None]):
        self._session = session
        self._on_message = on_message
        self._ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self._send_id = 0
        self._ping_task: Optional[asyncio.Task] = None

    async def connect(self, endpoint: str) -> None:
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
            try:
                await self.send("die")
            except Exception:
                pass
            await self._ws.close()

    def _decode_packet(self, data: bytes) -> list:
        if not data:
            return []
        header = data[0]
        if header == 0x45:
            return [msgpack.unpackb(data[1:], raw=False)]
        if header == 0xAE:
            extracted_id = struct.unpack_from(">I", data, 1)[0]
            msg = msgpack.unpackb(data[5:], raw=False)
            msg["id"] = extracted_id
            return [msg]
        if header == 0x58:
            return self._decode_batch(data[1:])
        if header == 0xB0:
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

    async def _ping_loop(self) -> None:
        try:
            while True:
                await asyncio.sleep(self.PING_INTERVAL)
                if self._ws and not self._ws.closed:
                    await self._ws.send_bytes(b"\xb0\x0b")
        except asyncio.CancelledError:
            pass
