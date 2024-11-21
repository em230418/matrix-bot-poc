#!/usr/bin/env python3

import logging

import asyncio

from nio import AsyncClient, MatrixRoom, RoomMessageText, AsyncClientConfig
from nio import ErrorResponse
import bot
import os

MATRIX_HOMESERVER = os.environ["MATRIX_HOMESERVER"]
MATRIX_USER = os.environ["MATRIX_USER"]
MATRIX_PASSWORD = os.environ["MATRIX_PASSWORD"]

bot.netsvc.init_logger()

async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
    print(
        f"Message received in room {room.display_name}\n"
        f"{room.user_name(event.sender)} | {event.body}"
    )


async def main() -> None:
    config = AsyncClientConfig(request_timeout=5, max_timeout_retry_wait_time=1)
    client = AsyncClient(MATRIX_HOMESERVER, MATRIX_USER)

    resp = await client.login(MATRIX_PASSWORD)
    if isinstance(resp, ErrorResponse):
        await client.close()
        raise Exception(resp)

    client.add_event_callback(message_callback, RoomMessageText)

    # If you made a new room and haven't joined as that user, you can use
    # await client.join("your-room-id")

    await client.room_send(
        # Watch out! If you join an old room you'll see lots of old messages
        room_id="!my-fave-room:example.org",
        message_type="m.room.message",
        content={"msgtype": "m.text", "body": "Hello world!"},
    )
    await client.sync_forever(timeout=30000)  # milliseconds


asyncio.run(main())
