# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'

    team_id = fields.Many2one(tracking=True)
    fully_invoiced = fields.Boolean(default=False)

    def create_invoice_new(self):
        for order in self:
            order.fully_invoiced = True
            inv_obj = self.env['account.move']
            ir_property_obj = self.env['ir.property']
            lines = []

            for line in order.order_line:
                account_id = False
                if line.product_id.id:
                    account_id = order.fiscal_position_id.map_account(
                        line.product_id.property_account_income_id or line.product_id.categ_id.property_account_income_categ_id).id
                if not account_id:
                    inc_acc = ir_property_obj.get('property_account_income_categ_id', 'product.category')
                    account_id = order.fiscal_position_id.map_account(inc_acc).id if inc_acc else False
                if not account_id:
                    raise UserError(
                        _(
                            'There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app, settings menu.') %
                        (self.product_id.name,))
                taxes = line.product_id.taxes_id.filtered(
                    lambda r: not order.company_id or r.company_id == order.company_id)
                if order.fiscal_position_id and taxes:
                    tax_ids = order.fiscal_position_id.map_tax(taxes).ids
                else:
                    tax_ids = taxes.ids

                lines.append((0, 0, {
                    'name': line.name,
                    # 'invoice_origin': order.name,
                    'account_id': account_id,
                    'price_unit': line.price_unit,
                    'quantity': line.product_uom_qty,
                    'discount': line.discount,
                    'product_uom_id': line.product_id.uom_id.id,
                    'product_id': line.product_id.id,
                    'tax_ids': [(6, 0, tax_ids)],
                    'analytic_account_id': order.analytic_account_id.id or False,
                })),

            invoice = inv_obj.create({
                # 'name': order.client_order_ref or order.name,
                'invoice_origin': order.name,
                'move_type': 'out_invoice',
                'ref': False,
                # 'account_id': order.partner_id.property_account_receivable_id.id,
                'partner_id': order.partner_invoice_id.id,
                'partner_shipping_id': order.partner_shipping_id.id,
                'currency_id': order.pricelist_id.currency_id.id,
                'invoice_payment_term_id': order.payment_term_id.id,
                'fiscal_position_id': order.fiscal_position_id.id or order.partner_id.property_account_position_id.id,
                'team_id': order.team_id.id,
                'user_id': order.user_id.id,
                'narration': order.note,
                'invoice_line_ids': lines,
            })
            # invoice.compute_taxes()
            invoice.message_post_with_view('mail.message_origin_link',
                                           values={'self': invoice, 'invoice_origin': order},
                                           subtype_id=self.env.ref('mail.mt_note').id)
            line.qty_invoiced = line.qty_invoiced + line.product_uom_qty
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'views': [[self.env.ref('account.view_move_form').id, 'form']],
            'target': 'current',
            'res_id': invoice.id,
        }


    def action_quotation_sent(self):
        if self.filtered(lambda so: so.state != 'draft'):
            raise UserError(_('Only draft orders can be marked as sent directly.'))
        for order in self:
            order.message_subscribe(partner_ids=order.partner_id.ids)
        self.write({'state': 'sent'})

    invoice_count = fields.Integer(string='Invoice Count', compute='_get_invoiced_new')
    def _get_invoiced_new(self):
        # The invoice_ids are obtained thanks to the invoice lines of the SO
        # lines, and we also search for possible refunds created directly from
        # existing invoices. This is necessary since such a refund is not
        # directly linked to the SO.
        for order in self:
            invoices = self.env['account.move'].search([('move_type', 'in',['out_invoice','out_refund']),('invoice_origin', 'ilike', self.name)])
            # order.invoice_ids = invoices
            order.invoice_count = len(invoices)

    def action_view_invoice(self):
        # invoices = self.mapped('invoice_ids')
        for rec in self:
            invoices = self.env['account.move'].search([('move_type', 'in',['out_invoice','out_refund']),('invoice_origin', 'ilike',rec.name)])
            print("invoices :> ",invoices)
            print("invoices :>",invoices)
            action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
            if len(invoices) > 1:
                action['domain'] = [('id', 'in', invoices.ids)]
            elif len(invoices) == 1:
                form_view = [(self.env.ref('account.view_move_form').id, 'form')]
                if 'views' in action:
                    action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
                else:
                    action['views'] = form_view
                action['res_id'] = invoices.id
            else:
                action = {'type': 'ir.actions.act_window_close'}

            context = {
                'default_move_type': 'out_invoice',
            }
            if len(self) == 1:
                context.update({
                    'default_partner_id': self.partner_id.id,
                    'default_partner_shipping_id': self.partner_shipping_id.id,
                    'default_invoice_payment_term_id': self.payment_term_id.id or self.partner_id.property_payment_term_id.id or self.env['account.move'].default_get(['invoice_payment_term_id']).get('invoice_payment_term_id'),
                    'default_invoice_origin': self.name,
                    'default_user_id': self.user_id.id,
                })
            action['context'] = context
        return action
