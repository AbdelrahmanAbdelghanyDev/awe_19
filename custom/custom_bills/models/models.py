# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomBills(models.Model):
    _inherit = 'purchase.order'

    bills_total = fields.Float(string="Bills Total", required=False, compute='_get_bills_total')
    bills_untaxed_total = fields.Float(string="Bills Untaxed Total", required=False, compute='_get_bills_total')
    remaining_amount = fields.Float(string="Remaining Amount", required=False, compute='_get_bills_total')
    remaining_untaxed_amount = fields.Float(string="Remaining Untaxed Amount", required=False, compute='_get_bills_total')

    @api.depends('invoice_ids', 'amount_total', 'amount_untaxed')
    def _get_bills_total(self):
        for rec in self:
            total = sum(i.amount_total for i in rec.invoice_ids)
            total_untaxed = sum(i.amount_untaxed for i in rec.invoice_ids)
            rec.bills_total = total
            rec.remaining_amount = rec.amount_total - total
            rec.bills_untaxed_total = total_untaxed
            rec.remaining_untaxed_amount = rec.amount_untaxed - total_untaxed
