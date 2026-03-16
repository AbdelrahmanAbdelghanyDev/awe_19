from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    # tag_ids = fields.Many2many('crm.tag', string="Tags")
    # tag_ids = fields.Many2many(comodel_name="crm.tag", relation="account_move_crm_lead", column1="account_move_1", column2="crm_lead_1", string="Tags", )
    executive_team_id = fields.Many2one('executive.team', string="Executive Team")
    revenue_team_id = fields.Many2one('revenue.team', string="Revenue Team")



class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'


    def unlimited_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        sale_orders.action_invoice_create()
        if self._context.get('open_invoices', False):
            return sale_orders.action_view_invoice()
        return {'type': 'ir.actions.act_window_close'}

    #
    # def create_invoices(self):
    #     res = self.unlimited_invoices()
    #     if res.get('domain') and res.get('domain')[0][0] == 'id':
    #         last_record = max(res.get('domain')[0][2])
    #         invoice = self.env['account.move'].search([('id', '=', last_record)])
    #         orders = self.env['sale.order'].search(
    #             [('company_id', '=', self.env.user.company_id.id)]).filtered(lambda l: l.name in invoice.origin)
    #
    #         # for lds in invoice.invoice_line_ids:
    #         #     lds.unlink()
    #         lines = []
    #         ir_property_obj = self.env['ir.property']
    #
    #         for order in orders:
    #             for line in order.order_line:
    #                 account_id = False
    #                 if line.product_id.id:
    #                     account_id = order.fiscal_position_id.map_account(
    #                         line.product_id.property_account_income_id or line.product_id.categ_id.property_account_income_categ_id).id
    #                 if not account_id:
    #                     inc_acc = ir_property_obj.get('property_account_income_categ_id', 'product.category')
    #                     account_id = order.fiscal_position_id.map_account(inc_acc).id if inc_acc else False
    #                 if not account_id:
    #                     raise UserError(
    #                         _(
    #                             'There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app, settings menu.') %
    #                         (self.product_id.name,))
    #                 taxes = line.product_id.taxes_id.filtered(
    #                     lambda r: not order.company_id or r.company_id == order.company_id)
    #                 if order.fiscal_position_id and taxes:
    #                     tax_ids = order.fiscal_position_id.map_tax(taxes).ids
    #                 else:
    #                     tax_ids = taxes.ids
    #                 invoiced_amt = 0
    #                 for inv in order.invoice_ids:
    #                     invoiced_amt += sum(
    #                         (inv_line.quantity if inv_line.product_id.id == line.product_id.id else 0) for inv_line in
    #                         inv.invoice_line_ids)
    #                 lines.append((0, 0, {
    #                     'name': line.name,
    #                     'origin': order.name,
    #                     'account_id': account_id,
    #                     'price_unit': line.price_unit,
    #                     'quantity': line.product_uom_qty - line.qty_invoiced if (
    #                             line.product_uom_qty - line.qty_invoiced > 0) else line.product_uom_qty,
    #                     'discount': line.discount,
    #                     'uom_id': line.product_id.uom_id.id,
    #                     'product_id': line.product_id.id,
    #                     'invoice_line_tax_ids': [(6, 0, tax_ids)],
    #                     'account_analytic_id': order.analytic_account_id.id or False,
    #                 })),
    #
    #         invoice.write({
    #             'invoice_line_ids': lines,
    #         })
    #         for order in orders:
    #             for line in order.order_line:
    #                 line.write({
    #                     'invoice_lines': [(4, inv_line.id) for inv_line in invoice.invoice_line_ids],
    #                 })
    #
    #         amount_tax = '0'
    #         # for order in orders:
    #         #     for l in order.order_line:
    #         #         amount_tax += sum(t.amount for t in l.product_id.taxes_id) * l.price_subtotal_new
    #         # for invoice_line in invoice.invoice_line_ids:
    #         #     amount_tax += sum(t.amount for t in invoice_line.product_id.taxes_id) * invoice_line.price_subtotal
    #         #
    #         # invoice.write({'amount_tax': amount_tax // 100})
    #         sign = invoice.move_type in ['in_refund', 'out_refund'] and -1 or 1
    #         invoice.write({'amount_total': invoice.amount_untaxed + invoice.amount_tax,
    #                        'amount_total_signed': (invoice.amount_untaxed + invoice.amount_tax) * sign})
    #     if res.get('res_id'):
    #         inv_update = self.env[res.get('res_model')].search([('id', '=', res.get('res_id'))], limit=1)
    #         sale = self.env['sale.order'].search([('name', '=', inv_update.origin)], limit=1)
    #         if sale:
    #             inv_update.write({
    #                 'tag_ids': [(6, 0, sale.tag_ids.ids)],
    #                 'executive_team_id': sale.executive_team_id.id,
    #                 'revenue_team_id': sale.revenue_team_id.id
    #             })
    #
    #     return res


    # new part todo
    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))

        if self.advance_payment_method == 'delivered':
            sale_orders._create_invoices(final=self.deduct_down_payments)
        else:
            # Create deposit product if necessary
            if not self.product_id:
                vals = self._prepare_deposit_product()
                self.product_id = self.env['product.product'].create(vals)
                self.env['ir.config_parameter'].sudo().set_param('sale.default_deposit_product_id', self.product_id.id)

            sale_line_obj = self.env['sale.order.line']
            for order in sale_orders:
                amount, name = self._get_advance_details(order)

                if self.product_id.invoice_policy != 'order':
                    raise UserError(_('The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
                if self.product_id.type != 'service':
                    raise UserError(_("The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
                taxes = self.product_id.taxes_id.filtered(lambda r: not order.company_id or r.company_id == order.company_id)
                tax_ids = order.fiscal_position_id.map_tax(taxes).ids
                analytic_tag_ids = []
                for line in order.order_line:
                    analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag in line.analytic_tag_ids]

                so_line_values = self._prepare_so_line(order, analytic_tag_ids, tax_ids, amount)
                so_line = sale_line_obj.create(so_line_values)
                self._create_invoice(order, so_line, amount)
        if self._context.get('open_invoices', False):
            return sale_orders.action_view_invoice()
        return {'type': 'ir.actions.act_window_close'}
