# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.constrains('product_line')
    def product_line_constrains(self):
        for rec in self:
            if len(rec.product_line) > 1:
                raise ValidationError(_('You are not allowed to more than one line in product line'))

    @api.onchange('product_line')
    def product_line_onchange(self):
        for rec in self:
            if len(rec.product_line) > 1:
                raise ValidationError(_('You are not allowed to more than one line in product line'))