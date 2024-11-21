#!/usr/bin/env python3

from typing import Dict

import logging

import asyncio

from nio import AsyncClient, MatrixRoom, RoomMessageText, AsyncClientConfig, AccountDataEvent
from nio import ErrorResponse
import bot
import os

MATRIX_HOMESERVER = os.environ["MATRIX_HOMESERVER"]
MATRIX_USER = os.environ["MATRIX_USER"]
MATRIX_PASSWORD = os.environ["MATRIX_PASSWORD"]

bot.netsvc.init_logger()

_logger = logging.getLogger(__name__)

class Bot:
    client: AsyncClient
    room_datas: Dict

    def __init__(self, room_datas: Dict):
        self.room_datas = room_datas

    def get_last_seen_date(self, room_id):
        room_data = self.room_datas[room_id]
        ["last_seen"]

    async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
        room_data = self.room_datas.get(room.room_id)
        if not room_data:

        # latest date = datetime.utcfromtimestamp(event.source['origin_server_ts'])
        # room id = room.room_id
        print(
            f"Message received in room {room.display_name}\n"
            f"{room.user_name(event.sender)} | {event.body}"
        )

        # TODo

    async def start(self):
        config = AsyncClientConfig(request_timeout=5, max_timeout_retry_wait_time=1)
        self.client = client = AsyncClient(MATRIX_HOMESERVER, MATRIX_USER, config=config)

        resp = await client.login(MATRIX_PASSWORD)
        if isinstance(resp, ErrorResponse):
            await client.close()
            raise Exception(resp)

        client.add_event_callback(message_callback, RoomMessageText)

a = False


async def account_data_callback(room: MatrixRoom, event: AccountDataEvent) -> None:
    from pprint import pprint
    pprint(event)

async def main() -> None:
    # TODO: какие комнаты надо смотреть?

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
