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


class CustomSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    no_of_waves = fields.Integer(default=1)  # Based on customer request.
    no_of_units = fields.Float(default=1)  # Based on customer request.
    # Based on customer request.
    price_subtotal_new = fields.Float(compute='_amount_subtotal_new')
    margin = fields.Float(compute='_compute_margin')
    margin_percentage = fields.Char(compute='_compute_margin')


    @api.depends('product_id')
    def _compute_margin(self):
        for rec in self:
            rec.margin = \
                rec.product_id.lst_price - rec.product_id.standard_price
            if rec.product_id.standard_price == 0:
                self.margin_percentage = 'Inf'
            else:
                rec.margin_percentage = str(
                    1.0 * (rec.margin / rec.product_id.standard_price) * 100.0)

    @api.depends('no_of_units', 'product_uom_qty', 'price_unit')
    def _amount_subtotal_new(self):
        for i in self:
            i.price_subtotal_new = \
                i.no_of_units * i.product_uom_qty * i.price_unit

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_ids', 'no_of_waves', 'price_subtotal_new',
                 'no_of_units')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(
                price * line.no_of_units * line.no_of_waves,
                line.order_id.currency_id,
                line.product_uom_qty,
                product=line.product_id,
                partner=line.order_id.partner_shipping_id
            )
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': line.price_subtotal_new * line.no_of_waves,
            })
