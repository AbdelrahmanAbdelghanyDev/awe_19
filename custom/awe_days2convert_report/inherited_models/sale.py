# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    crm_date = fields.Datetime(related='opportunity_id.create_date')

    days_to_convert = fields.Integer(compute='_compute_days_to_convert')

    @api.depends('crm_date', 'date_order')
    def _compute_days_to_convert(self):
        for rec in self:
            result = False
            if rec.crm_date and rec.date_order:
                diff = rec.date_order - rec.crm_date
                result = diff.days
            rec.days_to_convert = result
