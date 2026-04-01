from odoo import api, fields, models


class ResMethodology(models.Model):
    _name = 'res.methodology'
    _description = 'ResMethodology'

    name = fields.Char(required=True)
