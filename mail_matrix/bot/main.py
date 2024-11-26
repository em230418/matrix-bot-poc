#!/usr/bin/env python3

from typing import Dict

import logging

import asyncio
from datetime import datetime

from nio import AsyncClient, MatrixRoom, RoomMessageText, AsyncClientConfig, AccountDataEvent
from nio import ErrorResponse
import bot
import os
from bot.odoo_instance import OdooInstance

MATRIX_HOMESERVER = os.environ["MATRIX_HOMESERVER"]
MATRIX_USER = os.environ["MATRIX_USER"]
MATRIX_PASSWORD = os.environ["MATRIX_PASSWORD"]

bot.netsvc.init_logger()

_logger = logging.getLogger(__name__)


class Bot:
    client: AsyncClient
    room_datas: Dict

    def __init__(self, messaging_data: Dict):
        self.room_datas = messaging_data["room_datas"]

    def get_last_seen_date(self, room_id) -> datetime:
        last_seen = self.room_datas[room_id]["last_seen"]
        return datatime.utcfromtimestamp(last_seen)

    async def message_callback(room: MatrixRoom, event: RoomMessageText) -> None:
        last_seen_in_odoo = self.get_last_seen_date(room_id)
        message_date = datetime.utcfromtimestamp(event.source['origin_server_ts'])

        if message_date <= last_seen_in_odoo:
            _logger.debug(f"Ignoring message from {room.display_name} on date {message_date}")
            return

        # TODO: check if self. ignore it

        # latest date =
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


async def main() -> None:
    odoo = OdooInstance(bot.tools.config)
    await odoo.check()
    init_messaging_data = await odoo.init_messaging()

    bot = Bot(init_messaging_data)


    # TODO: какие комнаты надо смотреть?

    # If you made a new room and haven't joined as that user, you can use
    # await client.join("your-room-id")

    '''
    await client.room_send(
        # Watch out! If you join an old room you'll see lots of old messages
        room_id="!my-fave-room:example.org",
        message_type="m.room.message",
        content={"msgtype": "m.text", "body": "Hello world!"},
    )
    '''
    await client.sync_forever(timeout=30000)  # milliseconds


asyncio.run(main())
