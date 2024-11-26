from odoo import api, fields, models


class MailGuest(models.Model):
    _inherit = "mail.guest"

    matrix_bot = fields.Many2one("matrix.bot")
