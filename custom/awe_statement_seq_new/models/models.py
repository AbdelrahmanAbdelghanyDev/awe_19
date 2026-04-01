# -*- coding: utf-8 -*-

from odoo import models, fields, api


class accountBankStatementInh(models.Model):
    _inherit = 'account.bank.statement'

    name = fields.Char(string='Reference', copy=False, readonly=True, store=True)

    type = fields.Selection(
        string='Type',
        selection=[('in', 'Statement In'),
                   ('out', 'Statement Out'), ],
        required=False, default='in')

    @api.model
    def create(self, vals):
        res = super(accountBankStatementInh, self).create(vals)
        seq_code = ''
        if res.type == 'in':
            seq_code = 'account.bank.statement.in'
        elif res.type == 'out':
            seq_code = 'account.bank.statement.out'
        self_comp = self.with_company(res.company_id.id)
        res.name = self_comp.env['ir.sequence'].next_by_code(seq_code)

        return res
