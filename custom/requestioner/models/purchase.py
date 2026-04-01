# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from num2words import num2words


class PO(models.Model):
    _inherit = 'purchase.order'
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',
                                     )
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')
    payment_terms_details = fields.Text(string="Payment terms details", required=False, )
    source_doc = fields.Char(string="Source Document", required=False, )
    re_invoice_count = fields.Integer(compute="_recompute_invoice", string='# of Bills', copy=False, default=0,
                                      store=False)
    amount_to_text = fields.Text(
        store=True,
        compute='_amount_to_words'
    )

    @api.depends('amount_total')
    def _amount_to_words(self):
        for rec in self:
            if rec.partner_id:
                print("num 2 text :",rec.amount_total)
                print("num 2 text :",rec.currency_id.en_amount_to_text(rec.amount_total))
                # rec.amount_to_text = num2words(rec.amount_total)
                rec.amount_to_text = rec.currency_id.en_amount_to_text(rec.amount_total)

    @api.depends('order_line.price_total')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })

    def _recompute_invoice(self):
        for order in self:
            order.re_invoice_count = self.env['account.move'].search_count([('invoice_origin', '=', order.name)])

    def action_view_invoice(self ,invoices=False):
        '''
        This function returns an action that display existing vendor bills of given purchase order ids.
        When only one found, show the vendor bill immediately.
        '''
        action = self.env.ref('account.action_move_in_invoice_type')
        result = action.read()[0]
        # action = self.env.ref('egyptian_electronic_invoice.action_electronic_invoice_result').read()[0]
        # return action
        # override the context to get rid of the default filtering
        result['context'] = {'move_type': 'in_invoice', 'default_purchase_id': self.id}

        if len(self.invoice_ids) != 1:
            result['domain'] = "[('id', 'in', " + str(
                self.env['account.move'].search([('invoice_origin', '=', self.name)]).ids) + ")]"
            print("dddddwwww",result)
        if len(self.invoice_ids) == 1:
            res = self.env.ref('account.view_move_form')
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = self.invoice_ids.id
        result['context']['default_invoice_origin'] = self.name
        result['context']['default_reference'] = self.partner_ref
        return result


    def button_cancel(self):
        self.write({'state': 'cancel', 'mail_reminder_confirmed': False})


    # def update_methodology(self):
    #     for rec in self:
    #         for line in rec.order_line:
    #             methodolgy = self.env['estimation.methodology'].search([('name','=',line.methodology)],limit=1).id
    #             line.methodology_type_id = methodolgy
class CustomPurchaseLine(models.Model):
    _inherit = 'purchase.order.line'

    pr_number = fields.Many2one(comodel_name="sale.order", string="PR Number", required=False, )
    methodology = fields.Char(string="Methodology", required=False, )
    methodology_type_id = fields.Many2one('estimation.methodology',string="Methodology Type", required=False, )
    country = fields.Char(string="Country", required=False, )
    date_planned = fields.Datetime(string='Scheduled Date', required=False, index=True)
    product_uom = fields.Many2one('uom.uom', string='Product Unit of Measure', required=False)
    product_id = fields.Many2one('product.product', required=False, copy=False,
                                 default=lambda l: l.env['product.product'].search([], limit=1))
