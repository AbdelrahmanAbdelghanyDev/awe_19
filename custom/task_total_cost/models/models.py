# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # @api.depends('project_id.analytic_account_id')
    # def get_task_total_cost(self):
    #     for rec in self:
    #         journal_items = self.env['account.move.line'].search([('account_id.user_type_id.name', '=',
    #                                                                'Cost of Revenue'),
    #                                                               ('analytic_account_id', '=',
    #                                                                rec.project_id.analytic_account_id.id)])
    #         rec.task_total_cost = sum(journal_items.mapped('balance'))
    #         print('hhhhhhhhhh', rec.task_total_cost)


    task_total_cost = fields.Float(string="Total Cost", compute='get_task_total_cost')

    cost_waves = fields.Float(string="Cost / Waves", related='sale_order_id.wave_cost')

    total_value = fields.Float(string="Total Value", compute='get_task_total_value')

    cost_job_to_date = fields.Float(string="Cost Job To Date", compute='get_cost_job')

    time_cost_total = fields.Float(compute='get_time_cost_total' , store = True)

    @api.depends('timesheet_ids.unit_amount',
                 # 'timesheet_ids.employee_id.timesheet_cost'
                 )
    def get_time_cost_total(self):
        for rec in self:
            t=0
            f=0
            for r in rec.timesheet_ids:
                # t += r.employee_id.timesheet_cost
                f += r.unit_amount
            rec.time_cost_total = t * f


    @api.depends('time_cost_total','cost_waves')
    def get_cost_job(self):
        for rec in self:
            rec.cost_job_to_date = (rec.task_total_cost + rec.time_cost_total) / rec.cost_waves if rec.cost_waves != 0 else 0

    @api.depends('sale_order_id.amount_untaxed')
    def get_task_total_value(self):
        for rec in self:
            rec.total_value = float(rec.sale_order_id.amount_untaxed)

    @api.depends('revenue', 'total_value')
    def get_task_cost_ratio(self):
        for rec in self:
            rec.task_cost_ratio = rec.revenue / rec.total_value * 100 if rec.total_value != 0 else 0

    task_cost_ratio = fields.Float(string="Task Cost Ratio", compute='get_task_cost_ratio')

    cost_per_task = fields.Float(string="Cost per Task", compute='get_cost_per_task')

    @api.depends('task_total_cost', 'task_cost_ratio')
    def get_cost_per_task(self):
        for rec in self:
            rec.cost_per_task = rec.task_total_cost * (rec.task_cost_ratio/100)

