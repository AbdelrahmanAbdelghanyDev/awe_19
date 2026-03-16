# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountingMove(models.Model):
    _inherit = 'account.move'
    # _inherit = ['account.move', 'mail.thread', 'mail.activity.mixin']
    name = fields.Char(tracking=True)
    ref = fields.Char(tracking=True)
    journal_id = fields.Many2one(tracking=True)
    state = fields.Selection(tracking=True)
    # because message is not undersandable, we should do it in another way
    # line_id = fields.One2many(tracking=True)
    to_check = fields.Boolean(tracking=True)
    partner_id = fields.Many2one(tracking=True)
    amount = fields.Float(tracking=True)
    date = fields.Date(tracking=True)
    narration = fields.Text(tracking=True)
    company_id = fields.Many2one(tracking=True)
    balance = fields.Float(tracking=True)

    # def button_cancel(self):
    #     for rec in self:
    #         rec.message_post('<ul>Status: Posted &rArr; Unposted</ul>')
    #     return super(AccountingMove, self).button_cancel()


class Accounting(models.Model):
    _inherit = 'account.move.line'


    date_maturity = fields.Date(string='Due date', copy=False,
                                help="This field is used for payable and receivable journal entries. You can put the limit date for the payment of this line.")

    @api.model
    def play(self):
        records = self.search([('create_date', '>=', '2021-08-04 00:00:00')]).filtered(
            lambda l: l.journal_id.name in ['Customer Invoices', 'Vendor Bills'])
        for rec in records:
            rec.date_maturity = rec.invoice_id.date_due

    #
    def write(self, vals):
        if vals:
            message = ""

            for _key, _value in vals.items():
                if _key == 'account_id':
                    old_value = self.account_id.name
                    old_name = 'Account'
                    last_value = self.env['account.account'].search([('id', '=', _value)]).name
                    message += '<li>%s: %s &rArr; %s</li><br/>' % (old_name, old_value, last_value)

                elif _key == 'debit':
                    old_value = self.debit
                    old_name = 'Debit'
                    last_value = _value
                    message += '<li>%s: %s &rArr; %s</li><br/>' % (old_name, old_value, last_value)

                elif _key == 'credit':
                    old_value = self.credit
                    old_name = 'Credit'
                    last_value = _value
                    message += '<li>%s: %s &rArr; %s</li><br/>' % (old_name, old_value, last_value)

                elif _key == 'currency_id':
                    old_value = self.currency_id.name
                    old_name = 'Currency'
                    last_value = self.env['res.currency'].search([('id', '=', _value)]).name
                    message += '<li>%s: %s &rArr; %s</li><br/>' % (old_name, old_value, last_value)
                elif _key == 'amount_currency':
                    old_value = self.amount_currency
                    old_name = 'Amount Currency'
                    last_value = _value
                    message += '<li>%s: %s &rArr; %s</li><br/>' % (old_name, old_value, last_value)
                else:
                    pass
            # if message:
            #     self.move_id.message_post(message)
        res = super(Accounting, self).write(vals)
        return res
