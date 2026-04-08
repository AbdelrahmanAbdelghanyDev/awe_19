# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


def _get_years_selection(self):
    year_range = 2051
    return [(str(year), str(year)) for year in range(2018, year_range)]


class JobCardWizard(models.TransientModel):
    _name = 'job.card.wizard'

    # Fields
    analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', string='Analytic Account',
                                          required=True)
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
    def generate_job_card(self):
        domain = [('analytic_account_id', '=', self.analytic_account_id.id)]

        # sale_order = self.env['sale.order'].search([('analytic_account_id', '=', self.analytic_account_id.id)], limit=1)
        sale_order = self.env['sale.order'].search(domain)
        # , limit = 1
        vals = {}
        counter = 0
        for order in sale_order:
            for task in self.env['project.task'].search([('sale_order_id', '=', order.id)], limit=1):
                if not counter:
                    if self.env['cost.estimation'].search([('sale_order', '=', order.id)]):
                        # , limit = 1
                        for estimation in self.env['cost.estimation'].search([('sale_order', '=', order.id)]):
                            counter = 1
                            # , limit = 1
                            budget_line_values = []
                            wip_line_values = []
                            for line in estimation.cost_estimation_line:
                                budget_line_values.append((0, 0, {
                                    'display_type': 'line_section',
                                    'name': 'Direct Cost',
                                }))
                                wip_line_values.append((0, 0, {
                                    'display_type': 'line_section',
                                    'name': 'Direct Cost',
                                }))
                                break
                            list = []
                            for line in estimation.cost_estimation_line:
                                # if line.cost_item_cost_sp:
                                if line.cost_item.id not in [2150, 2161, 2148]:
                                    if not line.sudo().budgetary_position.account_ids:
                                        budget_line_values.append((0, 0, {
                                            'item_id': line.cost_item.id,
                                            'quantity': line.cost_item_quant_sp,
                                            'unit_cost': line.cost_item_unit_cost,
                                            'cost': line.cost_item_cost_sp,
                                        }))
                                        wip_line_values.append((0, 0, {
                                            'item_id': line.cost_item.id,
                                            'quantity': line.cost_item_quant_sp,
                                            'unit_cost': line.cost_item_unit_cost,
                                            'cost': line.cost_item_cost_sp,
                                        }))
                                    else:
                                        wip_account = []
                                        cost_account = []
                                        for budgetary_line in line.budgetary_position.account_ids:
                                            if budgetary_line.sudo().wip_account_check:
                                                wip_account.append(budgetary_line.id)
                                            if budgetary_line.sudo().cost_account_check:
                                                cost_account.append(budgetary_line.id)
                                        for budgetary_line in line.budgetary_position.account_ids:
                                            if budgetary_line not in list and line.cost_item not in list:
                                                if budgetary_line.sudo().cost_account_check or budgetary_line.sudo().wip_account_check:
                                                    total_budget = 0
                                                    for line2 in estimation.cost_estimation_line:
                                                        if line2.cost_item == line.cost_item:
                                                            total_budget += line2.cost_item_cost_sp
                                                    if not total_budget:
                                                        total_budget = line.cost_item_cost_sp
                                                    if cost_account and wip_account:
                                                        budget_line_values.append((0, 0, {
                                                            'item_id': line.cost_item.id,
                                                            'quantity': line.cost_item_quant_sp,
                                                            'unit_cost': line.cost_item_unit_cost,
                                                            'cost': total_budget,
                                                            'account_id': cost_account[0],
                                                            'wip_account_id': wip_account[0],
                                                        }))
                                                        wip_line_values.append((0, 0, {
                                                            'item_id': line.cost_item.id,
                                                            'quantity': line.cost_item_quant_sp,
                                                            'unit_cost': line.cost_item_unit_cost,
                                                            'cost': total_budget,
                                                            'account_id': cost_account[0],
                                                            'wip_account_id': wip_account[0],
                                                        }))
                                                    elif cost_account and not wip_account:
                                                        budget_line_values.append((0, 0, {
                                                            'item_id': line.cost_item.id,
                                                            'quantity': line.cost_item_quant_sp,
                                                            'unit_cost': line.cost_item_unit_cost,
                                                            'cost': total_budget,
                                                            'account_id': cost_account[0],
                                                        }))
                                                        wip_line_values.append((0, 0, {
                                                            'item_id': line.cost_item.id,
                                                            'quantity': line.cost_item_quant_sp,
                                                            'unit_cost': line.cost_item_unit_cost,
                                                            'cost': total_budget,
                                                            'account_id': cost_account[0],
                                                        }))
                                                    elif wip_account and not cost_account:
                                                        budget_line_values.append((0, 0, {
                                                            'item_id': line.cost_item.id,
                                                            'quantity': line.cost_item_quant_sp,
                                                            'unit_cost': line.cost_item_unit_cost,
                                                            'cost': total_budget,
                                                            'wip_account_id': wip_account[0],
                                                        }))
                                                        wip_line_values.append((0, 0, {
                                                            'item_id': line.cost_item.id,
                                                            'quantity': line.cost_item_quant_sp,
                                                            'unit_cost': line.cost_item_unit_cost,
                                                            'cost': total_budget,
                                                            'wip_account_id': wip_account[0],
                                                        }))
                                                    else:
                                                        budget_line_values.append((0, 0, {
                                                            'item_id': line.cost_item.id,
                                                            'quantity': line.cost_item_quant_sp,
                                                            'unit_cost': line.cost_item_unit_cost,
                                                            'cost': total_budget,
                                                        }))
                                                        wip_line_values.append((0, 0, {
                                                            'item_id': line.cost_item.id,
                                                            'quantity': line.cost_item_quant_sp,
                                                            'unit_cost': line.cost_item_unit_cost,
                                                            'cost': total_budget,
                                                        }))
                                                    list.append(budgetary_line)
                                                    list.append(line.cost_item)
                            # for time_line in estimation.time_estimation_ids:
                            #     budget_line_values.append((0, 0, {
                            #         'display_type': 'line_section',
                            #         'name': 'Time Cost',
                            #     }))
                            #     wip_line_values.append((0, 0, {
                            #         'display_type': 'line_section',
                            #         'name': 'Time Cost',
                            #     }))
                            #     break
                            # list = []
                            # for time_line in estimation.time_estimation_ids:
                            #     # if time_line.cost_item_cost_sp:
                            #     if time_line.cost_item.id not in [2150, 2161, 2148]:
                            #         if not time_line.sudo().budgetary_position.account_ids:
                            #             budget_line_values.append((0, 0, {
                            #                 'item_id': time_line.cost_item.id,
                            #                 'quantity': time_line.cost_item_quant_sp,
                            #                 'unit_cost': time_line.cost_item_unit_cost,
                            #                 'cost': time_line.cost_item_cost_sp,
                            #             }))
                            #             wip_line_values.append((0, 0, {
                            #                 'item_id': time_line.cost_item.id,
                            #                 'quantity': time_line.cost_item_quant_sp,
                            #                 'unit_cost': time_line.cost_item_unit_cost,
                            #                 'cost': time_line.cost_item_cost_sp,
                            #             }))
                            #         else:
                            #             wip_account = []
                            #             cost_account = []
                            #             for budgetary_line in time_line.budgetary_position.account_ids:
                            #                 if budgetary_line.sudo().wip_account_check:
                            #                     wip_account.append(budgetary_line.id)
                            #                 if budgetary_line.sudo().cost_account_check:
                            #                     cost_account.append(budgetary_line.id)
                            #             for budgetary_line in time_line.budgetary_position.account_ids:
                            #                 if budgetary_line not in list and time_line.cost_item not in list:
                            #                     if budgetary_line.sudo().cost_account_check or budgetary_line.sudo().wip_account_check:
                            #                         total_budget = 0
                            #                         for line2 in estimation.cost_estimation_line:
                            #                             if line2.cost_item == time_line.cost_item:
                            #                                 total_budget += line2.cost_item_cost_sp
                            #                         if not total_budget:
                            #                             total_budget = time_line.cost_item_cost_sp
                            #                         if cost_account and wip_account:
                            #                             budget_line_values.append((0, 0, {
                            #                                 'item_id': time_line.cost_item.id,
                            #                                 'quantity': time_line.cost_item_quant_sp,
                            #                                 'unit_cost': time_line.cost_item_unit_cost,
                            #                                 'cost': total_budget,
                            #                                 'account_id': cost_account[0],
                            #                                 'wip_account_id': wip_account[0],
                            #                             }))
                            #                             wip_line_values.append((0, 0, {
                            #                                 'item_id': time_line.cost_item.id,
                            #                                 'quantity': time_line.cost_item_quant_sp,
                            #                                 'unit_cost': time_line.cost_item_unit_cost,
                            #                                 'cost': total_budget,
                            #                                 'account_id': cost_account[0],
                            #                                 'wip_account_id': wip_account[0],
                            #                             }))
                            #                         elif cost_account and not wip_account:
                            #                             budget_line_values.append((0, 0, {
                            #                                 'item_id': time_line.cost_item.id,
                            #                                 'quantity': time_line.cost_item_quant_sp,
                            #                                 'unit_cost': time_line.cost_item_unit_cost,
                            #                                 'cost': total_budget,
                            #                                 'account_id': cost_account[0],
                            #                             }))
                            #                             wip_line_values.append((0, 0, {
                            #                                 'item_id': time_line.cost_item.id,
                            #                                 'quantity': time_line.cost_item_quant_sp,
                            #                                 'unit_cost': time_line.cost_item_unit_cost,
                            #                                 'cost': total_budget,
                            #                                 'account_id': cost_account[0],
                            #                             }))
                            #                         elif wip_account and not cost_account:
                            #                             budget_line_values.append((0, 0, {
                            #                                 'item_id': time_line.cost_item.id,
                            #                                 'quantity': time_line.cost_item_quant_sp,
                            #                                 'unit_cost': time_line.cost_item_unit_cost,
                            #                                 'cost': total_budget,
                            #                                 'wip_account_id': wip_account[0],
                            #                             }))
                            #                             wip_line_values.append((0, 0, {
                            #                                 'item_id': time_line.cost_item.id,
                            #                                 'quantity': time_line.cost_item_quant_sp,
                            #                                 'unit_cost': time_line.cost_item_unit_cost,
                            #                                 'cost': total_budget,
                            #                                 'wip_account_id': wip_account[0],
                            #                             }))
                            #                         else:
                            #                             budget_line_values.append((0, 0, {
                            #                                 'item_id': time_line.cost_item.id,
                            #                                 'quantity': time_line.cost_item_quant_sp,
                            #                                 'unit_cost': time_line.cost_item_unit_cost,
                            #                                 'cost': total_budget,
                            #                             }))
                            #                             wip_line_values.append((0, 0, {
                            #                                 'item_id': time_line.cost_item.id,
                            #                                 'quantity': time_line.cost_item_quant_sp,
                            #                                 'unit_cost': time_line.cost_item_unit_cost,
                            #                                 'cost': total_budget,
                            #                             }))
                            #                         list.append(budgetary_line)
                            #                         list.append(time_line.cost_item)

                            # Actual Lines
                            actual_line_values = []
                            actual_line_accounts = []
                            total_debit = 0
                            actual_net = 0
                            domain = [('analytic_account_id', '=', self.analytic_account_id.id),
                                      ('account_id.user_type_id.name', 'in', ['Cost of Revenue'])]
                            # , 'Current Assets'
                            if self.month_ids:
                                months = []
                                for month in self.month_ids:
                                    months.append(month.num)
                                domain += [('date_month', 'in', months)]
                            if self.year:
                                domain += [('date_year', '=', int(self.year))]
                            for journal_item in self.env['account.move.line'].sudo().search(domain):
                                if journal_item.account_id not in actual_line_accounts:
                                    actual_line_accounts.append(journal_item.account_id)
                            direct_cost = 0
                            for account in actual_line_accounts:
                                account_debit = 0
                                account_credit = 0
                                account_net = 0
                                direct_cost = 0
                                cogs_domain = [('analytic_account_id', '=', self.analytic_account_id.id),
                                               ('account_id.user_type_id.name', 'in', ['Cost of Revenue'])]
                                if self.month_ids:
                                    months = []
                                    for month in self.month_ids:
                                        months.append(month.num)
                                    cogs_domain += [('date_month', 'in', months)]
                                if self.year:
                                    cogs_domain += [('date_year', '=', int(self.year))]
                                for journal_item in self.env['account.move.line'].sudo().search(cogs_domain):
                                    direct_cost += journal_item.debit - journal_item.credit
                                domain = [('analytic_account_id', '=', self.analytic_account_id.id),
                                          ('account_id.user_type_id.name', 'in', ['Cost of Revenue', 'Current Assets'])]
                                if self.month_ids:
                                    months = []
                                    for month in self.month_ids:
                                        months.append(month.num)
                                    domain += [('date_month', 'in', months)]
                                if self.year:
                                    domain += [('date_year', '=', int(self.year))]
                                for journal_item in self.env['account.move.line'].sudo().search(domain):
                                    if account == journal_item.account_id:
                                        account_debit += journal_item.debit
                                        account_credit += journal_item.credit
                                        account_net += journal_item.debit - journal_item.credit
                                actual_line_values.append((0, 0, {
                                    'account_id': account.id,
                                    'debit': account_debit,
                                    'credit': account_credit,
                                    'net': account_net,
                                }))
                                total_debit += account_debit
                                actual_net += account_net
                            income = 0
                            income_domain = [('analytic_account_id', '=', self.analytic_account_id.id),
                                             ('account_id.user_type_id.name', '=', 'Income')]
                            if self.month_ids:
                                months = []
                                for month in self.month_ids:
                                    months.append(month.num)
                                income_domain += [('date_month', 'in', months)]
                            if self.year:
                                income_domain += [('date_year', '=', int(self.year))]
                            for journal_item in self.env['account.move.line'].sudo().search(income_domain):
                                income += journal_item.credit - journal_item.debit

                            # Actual Lines Calculations
                            actual_line_calc_values = []
                            actual_line_calc_accounts = []
                            domain = [('analytic_account_id', '=', self.analytic_account_id.id),
                                      ('account_id.user_type_id.name', 'in', ['Cost of Revenue', 'Current Assets'])]
                            if self.month_ids:
                                months = []
                                for month in self.month_ids:
                                    months.append(month.num)
                                domain += [('date_month', 'in', months)]
                            if self.year:
                                domain += [('date_year', '=', int(self.year))]
                            for journal_item in self.env['account.move.line'].sudo().search(domain):
                                if journal_item.account_id not in actual_line_calc_accounts:
                                    actual_line_calc_accounts.append(journal_item.account_id)
                            for account in actual_line_calc_accounts:
                                account_debit = 0
                                account_credit = 0
                                account_net = 0
                                domain = [('analytic_account_id', '=', self.analytic_account_id.id),
                                          ('account_id.user_type_id.name', 'in', ['Cost of Revenue', 'Current Assets'])]
                                if self.month_ids:
                                    months = []
                                    for month in self.month_ids:
                                        months.append(month.num)
                                    domain += [('date_month', 'in', months)]
                                if self.year:
                                    domain += [('date_year', '=', int(self.year))]
                                for journal_item in self.env['account.move.line'].sudo().search(domain):
                                    if account == journal_item.account_id:
                                        account_debit += journal_item.debit
                                        account_credit += journal_item.credit
                                        account_net += journal_item.debit - journal_item.credit
                                actual_line_calc_values.append((0, 0, {
                                    'account_id': account.id,
                                    'debit': account_debit,
                                    'credit': account_credit,
                                    'net': account_net,
                                }))

                            if task.stage_id.name == 'Recognition':
                                vals = {
                                    'analytic_account_id': self.analytic_account_id.id,
                                    'opportunity_name': order.opportunity_id.name,
                                    'client_name': order.opportunity_id.partner_id.name,
                                    'client_sector_id': order.opportunity_id.partner_id.sector_id.id,
                                    'revenue_bu_id': order.opportunity_id.revenue_bu.id,
                                    'sales_bu_id': order.opportunity_id.team_id.id,
                                    'user_id': order.opportunity_id.user_id.id,
                                    'tag_ids': order.tag_ids.ids,
                                    'project_status': 'closed',
                                    'project_type_id': order.project_type_id.id,
                                    'project_type': order.project_type_2,
                                    'project_methodology_id': order.methodology_id.id,
                                    'budget_line': budget_line_values,
                                    'actual_line': actual_line_values,
                                    'actual_line_calc': actual_line_calc_values,
                                    'budget_wip_line': wip_line_values,
                                    'revenue_recog': income,
                                    'direct_cost': direct_cost,
                                    'gm': income - direct_cost,
                                }
                            else:
                                vals = {
                                    'analytic_account_id': self.analytic_account_id.id,
                                    'opportunity_name': order.opportunity_id.name,
                                    'client_name': self.analytic_account_id.partner_id.name,
                                    'client_sector_id': order.opportunity_id.partner_id.sector_id.id,
                                    'revenue_bu_id': order.opportunity_id.revenue_bu.id,
                                    'sales_bu_id': order.opportunity_id.team_id.id,
                                    'user_id': order.opportunity_id.user_id.id,
                                    'tag_ids': order.tag_ids.ids,
                                    'project_status': 'open',
                                    'project_type_id': order.project_type_id.id,
                                    'project_type': order.project_type_2,
                                    'project_methodology_id': order.methodology_id.id,
                                    'budget_line': budget_line_values,
                                    'actual_line': actual_line_values,
                                    'actual_line_calc': actual_line_calc_values,
                                    'budget_wip_line': wip_line_values,
                                    'revenue_recog': income,
                                    'direct_cost': direct_cost,
                                    'gm': income - direct_cost,
                                }
                    else:
                        pass
                else:
                    raise ValidationError(_('Cost estimation is not exist!'))

        job_card = self.env['job.card'].sudo().create(vals)
        return {
            'name': 'Job Card by Analytic Account',
            'res_model': 'job.card',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('id', '=', job_card.id)]
        }
