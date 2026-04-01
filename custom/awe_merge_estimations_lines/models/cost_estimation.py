# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date


class CostEstimation(models.Model):
    _inherit = 'cost.estimation'


    def get_cost_estimation_line(self):
        cost_estimation_line = []
        for rec in self:
            for line in rec.cost_estimation_line:
                lines = (0, 0, {
                    'salable_product': line.salable_product.id,
                    'cost_item': line.cost_item.id,
                    'cost_item_description': line.cost_item_description,
                    'cost_item_type': line.cost_item_type,
                    'cost_item_quant_sp': line.cost_item_quant_sp,
                    'cost_item_cost_currency': line.cost_item_cost_currency,
                    # 'budgetary_position': line.budgetary_position.id,
                })
                cost_estimation_line.append(lines)
        return cost_estimation_line

    def get_time_estimation_ids(self):
        time_estimation_ids = []
        checked_sp = False
        for rec in self:
            if not checked_sp:
                for line in rec.time_estimation_ids:
                    lines = (0, 0, {
                        'salable_product': line.salable_product.id,
                        'sp_desc': line.sp_desc,
                        'sp_quant': line.sp_quant,
                        'cost_item': line.cost_item.id,
                        'cost_item_description': line.cost_item_description,
                        'cost_item_type': line.cost_item_type,
                        'cost_item_quant_sp': line.cost_item_quant_sp,
                        'cost_item_cost_currency': line.cost_item_cost_currency,
                    })
                    time_estimation_ids.append(lines)
                    checked_sp = True
            else:
                n = 0
                while n < len(rec.time_estimation_ids):
                    for sp in time_estimation_ids:
                        sp[2]['cost_item_cost_currency'] += rec.time_estimation_ids[n].cost_item_cost_currency
                        n += 1
        return time_estimation_ids

    def merge_cost_estimation_lines(self):
        self = self.sudo()
        vals = {
            'customer': self[0].customer.id,
            'opportunity': self[0].opportunity.id,
            'sales_team': self[0].sales_team.id,
            'sales_person': self[0].sales_person.id,
            'price_list': self[0].price_list.id,
            'fx': self[0].fx,
            'state': 'draft',
            'methodology_id': self[0].methodology_id.id,
            'estimate_date': datetime.now(),
            'budget_date_from': date.today(),
            'budget_date_to':  date.today(),
            'budget': self[0].budget,
            'company_id': self[0].company_id.id,
            'markup': 0,
            'research_type': self[0].research_type.id,
            'cost_estimation_line': self.get_cost_estimation_line(),
            'time_estimation_ids': self.get_time_estimation_ids(),
        }
        self.env['cost.estimation'].create(vals)




