from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    matrix_endpoint = fields.Char(index=True)
