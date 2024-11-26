from odoo import api, fields, models
from requests import request


class MatrixBot(models.Model):
    _name = "matrix.bot"
    _description = "Matrix Bot"

    name = fields.Char(required=True)
    endpoint_url = fields.Char(required=True, groups="base.group_system")
    access_token = fields.Char(groups="base.group_system")

    def _request(self, method, url, params=None):
        if not params:
            params = {}

        r = request(method, urljoin(self.endpoint_url, url), json=params, timeout=10)
        r.raise_for_status()
        return r

    def ping(self):
        self._request("GET", "/ping")
        return True

    def _message_post(self, body, author):
        return self.with_delay()._request("POST", "/message_post", {
            "body": body,
            "author": author,
        })
