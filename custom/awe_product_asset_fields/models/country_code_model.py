from odoo import fields, models, api


class CountryCode(models.Model):
    _name = 'country.code.model'
    _description = 'country Code Model'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
