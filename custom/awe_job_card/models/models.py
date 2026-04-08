# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_order_month = fields.Integer()
    date_order_year = fields.Integer()


class AccountAccount(models.Model):
    _inherit = 'account.account'

    cost_account_check = fields.Boolean(compute='compute_cost_account_check')
    wip_account_check = fields.Boolean(compute='compute_wip_account_check')

    @api.depends('code')
    def compute_cost_account_check(self):
        for rec in self:
            if rec.code[0] == '4':
                rec.cost_account_check = True
            else:
                rec.cost_account_check = False

    @api.depends('code')
    def compute_wip_account_check(self):
        for rec in self:
            if rec.code[0] == '1':
                rec.wip_account_check = True
            else:
                rec.wip_account_check = False


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    date_month = fields.Integer(compute='compute_date_month', store=True)
    date_year = fields.Integer(compute='compute_date_year', store=True)

    @api.depends('date')
    def compute_date_month(self):
        for rec in self:
            rec.date_month = rec.date.month

    @api.depends('date')
    def compute_date_year(self):
        for rec in self:
            rec.date_year = rec.date.year
