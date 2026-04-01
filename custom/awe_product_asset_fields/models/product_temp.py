# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTempInherit(models.Model):
    _inherit = 'product.template'

    is_asset = fields.Boolean()

    location_id_custom = fields.Many2one('location.code.model', string='Location')
    country_id_custom = fields.Many2one('country.code.model', string='Country')
    department_id_custom = fields.Many2one('department.code.model', string='Department')

    code_custom = fields.Integer(string='Code')

    @api.onchange('location_id_custom', 'country_id_custom', 'department_id_custom', 'code_custom')
    def _onchange_codes_fields(self):
        self.barcode = ''
        code = ''
        if self.country_id_custom:
            code += self.country_id_custom.code
        if self.department_id_custom:
            code += self.department_id_custom.code
        if self.location_id_custom:
            code += self.location_id_custom.code
        if self.code_custom:
            code += str(self.code_custom)
        self.barcode = code
