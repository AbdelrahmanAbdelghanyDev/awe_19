# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    @api.onchange('analytic_account_id')
    def _onchange_analytic_account_expense(self):
        if self.analytic_account_id:
            sale_order = self.env['sale.order'].search([('analytic_account_id', '=', self.analytic_account_id.id)])
            if sale_order:
                if sale_order.revenue_team_id:
                    self.analytic_tag_ids = [(6, 0, sale_order.revenue_team_id.analytic_tag_ids.ids)]

class CrmLead(models.Model):
    _inherit = 'crm.lead'


    def action_new_quotation(self):
        action = super(CrmLead,self).action_new_quotation()
        # Make the lead's Assigned Partner the quotation's Referrer.
        action['context']['default_revenue_bu_id'] = self.revenue_bu.id
        return action


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    revenue_bu_id = fields.Many2one('revenue.team', string="Revenue BU")

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('analytic_account_id')
    def _onchange_analytic_account(self):
        if self.analytic_account_id:
            sale_order = self.env['sale.order'].search([('analytic_account_id','=',self.analytic_account_id.id)])
            if sale_order:
                if sale_order.revenue_team_id:
                    self.analytic_tag_ids = [(6, 0, sale_order.revenue_team_id.analytic_tag_ids.ids)]



