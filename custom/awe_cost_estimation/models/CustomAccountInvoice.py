# -*- coding: utf-8 -*-

from odoo import models, fields, api

SEC = [
    ('A', 'A'),
    ('AB', 'AB'),
    ('BC1', 'BC1'),
    ('C1', 'C1'),
    ('C2', 'C2'),
    ('C1C2', 'C1C2'),
    ('C2D', 'C2D'),
    ('D', 'D'),
    ('E', 'E'),
    ('DE', 'DE'),
]




class CustomAccountInvoice(models.Model):
    _inherit = 'account.move'

    custom_description = fields.Char()
    custom_quantity = fields.Integer(compute='_compute_custom_quantity')
    custom_unit_price = fields.Float(compute='_compute_unit_price')

    @api.depends('invoice_line_ids')
    def _compute_custom_quantity(self):
        for record in self:
            total = 0
            for line in record.invoice_line_ids:
                total += line.quantity

            record.custom_quantity = total

    @api.depends('invoice_line_ids')
    def _compute_unit_price(self):
        for record in self:
            total = 0
            for line in record.invoice_line_ids:
                total += line.price_unit

            record.custom_unit_price = total

