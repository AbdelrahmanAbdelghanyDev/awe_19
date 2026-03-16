from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CustomAccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    name = fields.Char('Description', required=False)

    # def _get_sale_order_line(self, vals=None):
    #     result = dict(vals or {})
    #     if self.project_id:
    #         if result.get('so_line'):
    #             sol = self.env['sale.order.line'].browse([result['so_line']])
    #         else:
    #             sol = self.so_line
    #         if not sol:
    #             sol = self.env['sale.order.line'].search([
    #                 ('order_id.project_id', '=', self.account_id.id),
    #                 ('state', '=', 'sale'),
    #                 ('product_id.track_service', '=', 'timesheet'),
    #                 ('product_id.type', '=', 'service')],
    #                 limit=1)
    #         if sol:
    #             result.update(self._get_timesheet_cost(result))

    #     so_line = result.get('so_line', False) or self.so_line
    #     if not so_line and self.account_id and self.product_id and (self.product_id.expense_policy != 'no'):
    #         order_in_sale = \
    #             self.env['sale.order'].search(
    #                 [
    #                     ('project_id', '=', self.account_id.id),
    #                     ('state', '=', 'sale')
    #                 ],
    #                 limit=1
    #             )
    #         order = order_in_sale or self.env['sale.order'].search(
    #             [('project_id', '=', self.account_id.id)], limit=1)
    #         if not order:
    #             return result

    #         price = self._get_invoice_price(order)
    #         so_lines = self.env['sale.order.line'].search([
    #             ('order_id', '=', order.id),
    #             ('price_unit', '=', price),
    #             ('product_id', '=', self.product_id.id)])

    #         if so_lines:
    #             result.update({'so_line': so_lines[0].id})
    #         else:
    #             if order.state != 'sale':
    #                 raise UserError(
    #                     _('The Sale Order %s linked to the \
    #                         Analytic Account must be validated\
    #                          before registering expenses.') % order.name)
    #             order_line_vals = self._get_sale_order_line_vals(order, price)
    #             if order_line_vals:
    #                 so_line = self.env['sale.order.line'].create(
    #                     order_line_vals)
    #                 so_line._compute_tax_id()
    #                 result.update({'so_line': so_line.id})
    #     return result

    #
    # def _sale_postprocess(self, values, additional_so_lines=None):

    #     if self.project_id:
    #         if 'so_line' in values:
    #             sol = self.env['sale.order.line'].browse([result['so_line']])
    #         else:
    #             sol = self.so_line
    #         if not sol:
    #             sol = self.env['sale.order.line'].search([
    #                 ('order_id.project_id', '=', self.account_id.id),
    #                 ('state', '=', 'sale'),
    #                 ('product_id.track_service', '=', 'timesheet'),
    #                 ('product_id.type', '=', 'service')],
    #                 limit=1)
    #         if sol:
    #             result.update(self._get_timesheet_cost(result))

    #     if 'so_line' not in values:  # allow to force a False value for so_line
    #         self.with_context(
    #             sale_analytic_norecompute=True)._sale_determine_order_line()

    #     if any(field_name in values for field_name in self._sale_get_fields_delivered_qty()):
    #         if not self._context.get('sale_analytic_norecompute'):
    #             so_lines = self.sudo().filtered(lambda aal: aal.so_line).mapped('so_line')
    #             if additional_so_lines:
    #                 so_lines |= additional_so_lines
    #             so_lines.sudo()._analytic_compute_delivered_quantity()

    #     if self.project_id:
    #         if result.get('so_line'):
    #             sol = self.env['sale.order.line'].browse([result['so_line']])
    #         else:
    #             sol = self.so_line
    #         if not sol:
    #             sol = self.env['sale.order.line'].search([
    #                 ('order_id.project_id', '=', self.account_id.id),
    #                 ('state', '=', 'sale'),
    #                 ('product_id.track_service', '=', 'timesheet'),
    #                 ('product_id.type', '=', 'service')],
    #                 limit=1)
    #         if sol:
    #             result.update(self._get_timesheet_cost(result))


    def _sale_postprocess(self, values, additional_so_lines=None):
        print()
        if 'so_line' not in values:  # allow to force a False value for so_line
            self.with_context(
                sale_analytic_norecompute=True)._sale_determine_order_line()

        if any(field_name in values for field_name in self._sale_get_fields_delivered_qty()):
            if not self._context.get('sale_analytic_norecompute'):
                so_lines = self.sudo().filtered(lambda aal: aal.so_line).mapped('so_line')
                if additional_so_lines:
                    so_lines |= additional_so_lines
                so_lines.sudo()._analytic_compute_delivered_quantity()
