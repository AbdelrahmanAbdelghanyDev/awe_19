# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CurrencyChange(models.Model):

    _inherit = 'account.move'

    @api.onchange('line_ids')
    def onch_amoun(self):
        if self.line_ids:
            for line in self.line_ids:
                if line.currency_id.id and line.currency_id.id != self.company_id.currency_id.id:
                    if self.env['res.currency.rate'].search([('name', '<=', self.date),('currency_id', '=', line.currency_id.id),('company_id', '=', self.company_id.id)]):
                        rate = self.env['res.currency.rate'].search([('name', '<=', self.date),('currency_id', '=', line.currency_id.id),('company_id', '=', self.company_id.id)],order="name")[-1].rate
                        print(rate)
                        if line.amount_currency > 0 and rate != 0:
                            line.debit = line.amount_currency / rate

                        if line.amount_currency < 0 and rate != 0:
                            line.credit = abs(line.amount_currency / rate)

                        else:
                            pass
                    else:
                        line.debit = line.amount_currency

