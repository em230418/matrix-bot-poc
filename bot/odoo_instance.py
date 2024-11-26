# TODO: использовать функционал mail.guest
import logging


from urllib.parse import urljoin
from uuid import uuid4
from aiohttp import ClientSession, ClientTimeout


_logger = logging.getLogger(__name__)

class OdooInstance:
    def __init__(self, config):
        self.access_token = config["odoo_guest_access_token"]
        self.endpoint = config["odoo_endpoint"]
        self.timeout = ClientTimeout(config["odoo_request_timeout"])

    async def post(self, method, params=None):
        if not params:
            params = {}

        async with ClientSession(self.endpoint, timeout=self.timeout) as session:
            payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": params,
                "id": str(uuid4()),
            }
            async with session.post(method, json=payload) as resp:
                if resp.status != 200:
                    raise Exception(await resp.text())
                return (await resp.json())["result"]

    async def check(self):
        _logger.info(f"Using endpoint {self.endpoint}")
        version_info = await self.post("/web/webclient/version_info")
        _logger.info(f"Odoo {version_info['server_version']}")

    async def init_messaging(self):
        return await self.post("/mail/matrix/init_messaging")
