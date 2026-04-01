# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InvoicePivot(models.Model):
    _inherit = 'account.move'

    paid_bills = fields.Integer("Paid", compute='_compute_paid_bills', store=True, readonly=True)

    @api.depends('state')
    def _compute_paid_bills(self):
        for rec in self:
            rec.paid_bills = rec.state == 'paid'


class POtoEntry(models.Model):
    _inherit = 'purchase.order'

    client = fields.Many2one(comodel_name="res.partner", string="Client", required=False, )

    payment_terms_details = fields.Char(string="Payment terms details", required=False, )
    date_planned = fields.Datetime(string='Scheduled Date', required=False, index=True)

    # @api.multi
    # def copy(self, default=None):
    #     return super(POtoEntry, self).copy(default=default)

    def button_approve(self, force=False):
        for order in self:
            # if order.state not in ['draft', 'sent']:
            #     continue
            # order._add_supplier_to_product()
            # Deal with double validation process
            #
            # new commented part

            # if order.company_id.po_double_validation == 'one_step' \
            #         or (order.company_id.po_double_validation == 'two_step' \
            #             and order.amount_total < self.env.user.company_id.currency_id.compute(
            #             order.company_id.po_double_validation_amount, order.currency_id)) \
            #         or order.user_has_groups('purchase.group_purchase_manager'):
            #     order.button_approve()
            # else:
            #     order.write({'state': 'to approve'})
        # new
            move = self.env['account.move']
            move_data = {
                'date': order.date_order,
                'ref': order.name,
                'currency_id': order.currency_id.id,
            }
            if self.env.company.name == 'AWE Egypt':
                move_data['journal_id'] = 11
            elif self.env.company.name == 'AWE KSA':
                move_data['journal_id'] = 19
            elif self.env.company.name == 'AWE UAE':
                move_data['journal_id'] = 28
            move_id = move.create(move_data)

            debit_account_id = 0
            if self.env.company.name == 'AWE Egypt':
                debit_account_id = 3227
            elif self.env.company.name == 'AWE KSA':
                debit_account_id = 5024
            elif self.env.company.name == 'AWE UAE':
                debit_account_id = 6316

            credit_account_id = 0
            if self.env.company.name == 'AWE Egypt':
                credit_account_id = 3292
            elif self.env.company.name == 'AWE KSA':
                credit_account_id = 5084
            elif self.env.company.name == 'AWE UAE':
                credit_account_id = 7948

            move_lines = []
            for line in order.order_line:
                move_lines.extend([
                    (0, 0, {'account_id': debit_account_id, 'partner_id': order.partner_id.id,
                            'name': order.name,
                            'analytic_account_id': line.account_analytic_id.id,
                            'debit': order.currency_id._convert(line.price_subtotal,
                                                                self.env.company.currency_id,
                                                                self.env.company, order.date_order),
                            'currency_id': order.currency_id.id,
                            'amount_currency': line.price_subtotal,
                            'credit': 0
                            }),
                    (0, 0, {'account_id': credit_account_id, 'partner_id': order.partner_id.id,
                            'name': order.name,
                            'currency_id': order.currency_id.id, 'debit': 0,
                            'analytic_account_id': line.account_analytic_id.id,
                            'amount_currency': -1 * line.price_subtotal,
                            'credit': order.currency_id._convert(line.price_subtotal,
                                                                 self.env.company.currency_id,
                                                                 self.env.company, order.date_order),
                            })])
            move_id.line_ids = move_lines
            order.state = 'purchase'
        return True
        # old todo 15/11/2022
        # move = self.env['account.move']
        # move_data = {
        #     'date': self.date_order,
        #     'ref': self.name,
        # }
        # if self.env.user.company_id.name == 'AWE Egypt':
        #     move_data['journal_id'] = 11
        # elif self.env.user.company_id.name == 'AWE KSA':
        #     move_data['journal_id'] = 19
        # elif self.env.user.company_id.name == 'AWE UAE':
        #     move_data['journal_id'] = 28
        # move_id = move.create(move_data)
        #
        # debit_account_id = 0
        # if self.env.user.company_id.name == 'AWE Egypt':
        #     debit_account_id = 3227
        # elif self.env.user.company_id.name == 'AWE KSA':
        #     debit_account_id = 5024
        # elif self.env.user.company_id.name == 'AWE UAE':
        #     debit_account_id = 6316
        #
        # credit_account_id = 0
        # if self.env.user.company_id.name == 'AWE Egypt':
        #     credit_account_id = 3292
        # elif self.env.user.company_id.name == 'AWE KSA':
        #     credit_account_id = 5084
        # elif self.env.user.company_id.name == 'AWE UAE':
        #     credit_account_id = 7948
        #
        # move_id.line_ids = [
        #     (0, 0, {'account_id': debit_account_id, 'partner_id': self.partner_id.id,
        #             'analytic_account_id': self.order_line[0].account_analytic_id.id if len(
        #                 self.order_line.ids) > 1 else self.order_line.account_analytic_id.id,
        #             'debit': self.amount_untaxed,
        #             'currency_id': self.currency_id.id,
        #             'amount_currency': self.amount_untaxed,
        #             'credit': 0}),
        #     (0, 0, {'account_id': credit_account_id, 'partner_id': self.partner_id.id,
        #             'currency_id': self.currency_id.id, 'debit': 0,
        #             'analytic_account_id': self.order_line[0].account_analytic_id.id if len(
        #                 self.order_line.ids) > 1 else self.order_line.account_analytic_id.id,
        #             'amount_currency': -1 * self.amount_untaxed,
        #             'credit': self.amount_untaxed, })]
        # move_id.line_ids._onchange_amount_currency()
        #
        # self.state='purchase'
        # return True


    def button_confirm(self):
        # self.button_done()
        for order in self:
            print("button_confirm :> ")
            if order.state not in ['draft', 'sent']:
                continue
            # order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step' \
                    or (order.company_id.po_double_validation == 'two_step' \
                        and order.amount_total < self.env.company.currency_id.compute(
                        order.company_id.po_double_validation_amount, order.currency_id)) \
                    or order.user_has_groups('purchase.group_purchase_manager'):
                # order.button_approve()
                self.state = 'purchase'
            else:
                order.write({'state': 'to approve'})

        #     print("ddddddddd")
        #     move = self.env['account.move']
        #     move_data = {
        #         'date': self.date_order,
        #         'ref': self.name,
        #     }
        #     if self.env.company.name == 'AWE Egypt':
        #         move_data['journal_id'] = 11
        #     elif self.env.company.name == 'AWE KSA':
        #         move_data['journal_id'] = 19
        #     elif self.env.company.name == 'AWE UAE':
        #         move_data['journal_id'] = 28
        #     move_id = move.create(move_data)
        #
        #     debit_account_id = 0
        #     if self.env.company.name == 'AWE Egypt':
        #         debit_account_id = 3227
        #     elif self.env.company.name == 'AWE KSA':
        #         debit_account_id = 5024
        #     elif self.env.company.name == 'AWE UAE':
        #         debit_account_id = 6316
        #
        #     credit_account_id = 0
        #     if self.env.company.name == 'AWE Egypt':
        #         credit_account_id = 3292
        #     elif self.env.company.name == 'AWE KSA':
        #         credit_account_id = 5084
        #     elif self.env.company.name == 'AWE UAE':
        #         credit_account_id = 7948
        #
        #     move_id.line_ids = [
        #         (0, 0, {'account_id': debit_account_id, 'partner_id': self.partner_id.id,
        #                 'analytic_account_id': self.order_line[0].account_analytic_id.id if len(
        #                     self.order_line.ids) > 1 else self.order_line.account_analytic_id.id,
        #                 'debit': self.amount_untaxed,
        #                 'currency_id': self.currency_id.id,
        #                 'amount_currency': self.amount_untaxed,
        #                 'credit': 0}),
        #         (0, 0, {'account_id': credit_account_id, 'partner_id': self.partner_id.id,
        #                 'currency_id': self.currency_id.id, 'debit': 0,
        #                 'analytic_account_id': self.order_line[0].account_analytic_id.id if len(
        #                     self.order_line.ids) > 1 else self.order_line.account_analytic_id.id,
        #                 'amount_currency': -1 * self.amount_untaxed,
        #                 'credit': self.amount_untaxed, })]
        #     # move_id.line_ids._onchange_amount_currency()
        #     print("move_id :> ",move_id)
        # return True
