# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


def _get_years_selection(self):
    year_range = 2051
    return [(str(year), str(year)) for year in range(2018, year_range)]


class RevenueBUWizard(models.TransientModel):
    _name = 'revenue.bu.wizard'

    # Fields
    # analytic_tag_ids = fields.Many2many(comodel_name="account.analytic.tag", string="Analytic Tags", required=True)
    # month = fields.Selection(
    #     [
    #         ('1', 'January'),
    #         ('2', 'February'),
    #         ('3', 'March'),
    #         ('4', 'April'),
    #         ('5', 'May'),
    #         ('6', 'June'),
    #         ('7', 'July'),
    #         ('8', 'August'),
    #         ('9', 'September'),
    #         ('10', 'October'),
    #         ('11', 'November'),
    #         ('12', 'December')
    #     ])
    month_ids = fields.Many2many(comodel_name='res.month', string='Month')
    year = fields.Selection(selection=_get_years_selection)

    # Methods
    # def generate_revenue_bu(self):
    #     domain = [('analytic_tag_ids', 'in', self.analytic_tag_ids.ids)]
    #     if self.month_ids:
    #         months = []
    #         for month in self.month_ids:
    #             months.append(month.num)
    #         domain += [('date_month', 'in', months)]
    #     if self.year:
    #         domain += [('date_year', '=', int(self.year))]
    #
    #     journal_items = self.env['account.move.line'].search(domain)
    #     revenue_bus = []
    #     exist_analytic_accounts = []
    #     for journal_item in journal_items:
    #         vals = {}
    #         if journal_item.analytic_account_id not in exist_analytic_accounts:
    #             if journal_item.analytic_account_id:
    #                 # New Version
    #                 domain = [('analytic_tag_ids', 'in', self.analytic_tag_ids.ids),
    #                           ('analytic_account_id', '=', journal_item.analytic_account_id.id)]
    #                 if self.month_ids:
    #                     months = []
    #                     for month in self.month_ids:
    #                         months.append(month.num)
    #                     domain += [('date_month', 'in', months)]
    #                 if self.year:
    #                     domain += [('date_year', '=', int(self.year))]
    #                 journal_items2 = self.env['account.move.line'].search(domain)
    #                 #
    #
    #                 # Last Version
    #                 # journal_items2 = self.env['account.move.line'].search(
    #                 #     [('analytic_account_id', '=', journal_item.analytic_account_id.id)])
    #                 income = 0
    #                 cost_of_revenue = 0
    #                 for journal_item2 in journal_items2:
    #                     project_type_id = 0
    #                     project_type_2 = 0
    #                     for sale in self.env['sale.order'].search(
    #                             [('analytic_account_id', '=', journal_item2.analytic_account_id.id)], limit=1):
    #                         project_type_id = sale.project_type_id.id
    #                         project_type_2 = sale.project_type_2
    #                     if journal_item2.account_id.user_type_id.name == 'Income':
    #                         income += journal_item2.credit - journal_item2.debit
    #                     if journal_item2.account_id.user_type_id.name == 'Cost of Revenue':
    #                         cost_of_revenue += journal_item2.debit - journal_item2.credit
    #                     if journal_item2.account_id.user_type_id.name == 'Income' or journal_item2.account_id.user_type_id.name == 'Cost of Revenue':
    #                         vals = {
    #                             'analytic_account_id': journal_item2.analytic_account_id.id,
    #                             'analytic_tag_ids': journal_item2.analytic_tag_ids.ids,
    #                             # 'date_month': journal_item2.date_month,
    #                             # 'month_id': self.env['res.month'].search([('num', '=', journal_item2.date_month)], limit=1).id,
    #                             'revenue': income,
    #                             'revenue_cost': cost_of_revenue,
    #                             'project_type_id': project_type_id,
    #                             'project_type_2': project_type_2,
    #                             # 'gm': income - cost_of_revenue,
    #                             # 'gm_percentage': ((income - cost_of_revenue) / income) * 100,
    #                         }
    #                 if vals:
    #                     revenue_bu = self.env['revenue.bu'].sudo().create(vals)
    #                     exist_analytic_accounts.append(journal_item.analytic_account_id)
    #                     revenue_bus.append(revenue_bu.id)
    #     return {
    #         'name': 'Job Card by Analytic Tag',
    #         'res_model': 'revenue.bu',
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'tree',
    #         'domain': [('id', 'in', revenue_bus)]
    #     }
