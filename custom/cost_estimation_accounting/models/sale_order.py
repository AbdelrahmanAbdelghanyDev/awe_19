# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class CostEstimationQuotation(models.Model):
    _inherit = 'sale.order'
    # budget = fields.Many2one('crossovered.budget',string="Budget", readonly=True)
    # budget = fields.Many2one('crossovered.budget',string="Budget", readonly=True)

    def action_confirm(self):
        res = super(CostEstimationQuotation, self).action_confirm()
        if not self.analytic_account_id:
            raise ValidationError(_("There is NO Analytical Account for this Quotation"))
        budget_line_list = []
        line_list = []
        general_budget_id = {3: 310, 4: 311, 5: 312}
        if self.cost_estimation_ref:

            # for rec in self.cost_estimation_ref.cost_estimation_line:
            #     if rec.budgetary_position.id not in line_list and (rec.budgetary_position.id != False):
            #         line_list.append(rec.budgetary_position.id)

            for item in line_list:
                total_budgetary_list = []
                # for line in self.cost_estimation_ref.cost_estimation_line:
                #     if item == line.budgetary_position.id:
                #         total_budgetary_list.append(line.total_cost_item_cost)

                budget_line_list.append((0, 0, {'general_budget_id': item,
                                                'analytic_account_id': self.analytic_account_id.id,
                                                'date_from': self.cost_estimation_ref.budget_date_from,
                                                'date_to': self.cost_estimation_ref.budget_date_to,
                                                'planned_amount': sum(total_budgetary_list)}))


            budget_line_list.append((0, 0, {'general_budget_id': general_budget_id[self.company_id.id] ,
                                            'analytic_account_id': self.analytic_account_id.id,
                                            'date_from': self.cost_estimation_ref.budget_date_from,
                                            'date_to': self.cost_estimation_ref.budget_date_to,
                                            'planned_amount': self.third_party_cost}))
            # if line_list != []:
                # budget = self.env['crossovered.budget'].search([]).create({'name':"%s - %s"%(self.name,self.cost_estimation_ref.seq),
                #                                                   'date_from':self.cost_estimation_ref.budget_date_from,
                #                                                   'date_to':self.cost_estimation_ref.budget_date_to,
                #                                                   'user_id':self.user_id.id,
                #                                                   'cost_estimation_id':self.cost_estimation_ref.id,
                #                                                   'crossovered_budget_line':budget_line_list})
                # self.budget = budget.id
                # self.cost_estimation_ref.budget = self.budget

        else:
            print(" company :> ",self.company_id.id)
            print("general_budget_id[self.company_id.id] :> ",general_budget_id[self.company_id.id])
            budget_line_list.append((0, 0, {'general_budget_id': general_budget_id[self.company_id.id] ,
                                            'analytic_account_id': self.analytic_account_id.id,
                                            'date_from': datetime.strptime(str(self.date_order), "%Y-%m-%d %H:%M:%S").date(),
                                            'date_to':datetime.strptime(str(self.date_order), "%Y-%m-%d %H:%M:%S").date(),
                                            'planned_amount': self.third_party_cost}))
            # budget = self.env['crossovered.budget'].search([]).create({'name':"%s"%(self.name),
            #                                                            'date_from': datetime.strptime(str(self.date_order), "%Y-%m-%d %H:%M:%S").date(),
            #                                                            'date_to':datetime.strptime(str(self.date_order), "%Y-%m-%d %H:%M:%S").date(),
            #                                                            'user_id':self.user_id.id,
            #                                                            'cost_estimation_id':self.cost_estimation_ref.id,
            #                                                            'crossovered_budget_line':budget_line_list})
            # self.budget = budget.id
        return res