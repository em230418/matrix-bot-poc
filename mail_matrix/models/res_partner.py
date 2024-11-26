from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    matrix_user_id = fields.Char(index=True)
