from odoo import fields, models, api


class LocationCode(models.Model):
    _name = 'location.code.model'
    _description = 'Location Code Model'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
