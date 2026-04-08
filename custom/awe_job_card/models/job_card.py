# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import json


class JobCard(models.Model):
    _name = 'job.card'
    _description = 'Job Card by Analytic Account'
    _rec_name = 'analytic_account_id'

    # Fields
    # General Info.
    analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', string='Analytic Account',
                                          required=True)
    opportunity_name = fields.Char(string='Opportunity Name')
    client_name = fields.Char(string='Client Name')
    client_sector_id = fields.Many2one(comodel_name='sector', string='Client Sector')
    revenue_bu_id = fields.Many2one(comodel_name='revenue.team', string='Revenue BU')
    sales_bu_id = fields.Many2one(comodel_name='crm.team', string='Sales BU')
    user_id = fields.Many2one(comodel_name='res.users', string='Sales Person')
    tag_ids = fields.Many2many(comodel_name='crm.tag', string='Client Type')
    project_status = fields.Selection(selection=[
        ('open', 'Open'),
        ('closed', 'Closed')
    ], string='Project Status')
    project_type_id = fields.Many2one(comodel_name='res.project.type', strin='Project Type')
    project_type = fields.Selection(selection=[
        ('adhoc', 'Adhoc'),
        ('tracker', 'Tracker'),
        ('waves', 'Waves'),
        ('syndicated', 'Syndicated')
    ], string='Project Type')
    project_methodology_id = fields.Many2one(comodel_name='res.methodology', string='Project Methodology')

    # Accounting Info.
    budget_line = fields.One2many(comodel_name='job.card.budget.line', inverse_name='job_card_id')
    actual_line = fields.One2many(comodel_name='actual.line', inverse_name='job_card_id')
    actual_line_calc = fields.One2many(comodel_name='actual.line.calc', inverse_name='job_card_id')
    actual_net = fields.Float(string='Actual Net', compute='compute_actual_net')
    budget_wip_line = fields.One2many(comodel_name='budget.wip.line', inverse_name='job_card_id')

    revenue_recog = fields.Float(string='Revenue Recog')
    direct_cost = fields.Float(string='Direct Cost')
    # , compute='compute_direct_cost')
    gm = fields.Float(string='GM')
    # , compute='compute_gm')
    gm_percentage = fields.Char(string='GM Percentage', compute='compute_gm_percentage')
    time_cost = fields.Float(string='Time Cost')
    op = fields.Float(string='OP')

    # Methods
    @api.depends('actual_line')
    def compute_actual_net(self):
        for rec in self:
            actual_net = 0
            for actual_line in rec.actual_line:
                actual_net += actual_line.debit - actual_line.credit
            rec.actual_net = actual_net

    # @api.depends('budget_line')
    # def compute_direct_cost(self):
    #     for rec in self:
    #         rec.direct_cost = 0
    #         for line in rec.budget_line:
    #             if line.account_id.cost_account_check:
    #                 rec.direct_cost += line.actual_net
    #
    # @api.depends('revenue_recog', 'direct_cost')
    # def compute_gm(self):
    #     for rec in self:
    #         rec.gm = rec.revenue_recog - rec.direct_cost

    @api.depends('revenue_recog', 'gm')
    def compute_gm_percentage(self):
        for rec in self:
            if rec.revenue_recog:
                rec.gm_percentage = str(round(((rec.gm / rec.revenue_recog) * 100), 2)) + '%'
            else:
                rec.gm_percentage = False


class BudgetLine(models.Model):
    _name = 'job.card.budget.line'
    _description = 'Budget Lines'
    _rec_name = 'item_id'

    # Fields
    job_card_id = fields.Many2one(comodel_name='job.card')
    name = fields.Char(string=' ')
    display_type = fields.Selection([
        ('line_section', 'Section'),
        ('line_note', 'Note'),
    ], default=False, help="Technical field for UX purpose.")
    item_id = fields.Many2one(comodel_name='product.template', string='Item')
    quantity = fields.Float(string='Quantity')
    unit_cost = fields.Float(string='Unit Cost')
    cost = fields.Float(string='Budget')
    account_id = fields.Many2one(comodel_name='account.account', string='Actual Account')
    actual_net = fields.Float(string='Actual Net', compute='compute_actual_net')
    variance = fields.Float(string='Actual Variance', compute='compute_variance')
    variance_percentage = fields.Char(string='Actual Variance Percentage', compute='compute_variance_percentage')
    over_under_budget = fields.Selection(string='Over/Under Budget (Actual)',
                                         selection=[('under', 'Under Budget'),
                                                    ('equal', 'Equal Budget'),
                                                    ('over', 'Over Budget')], compute='compute_over_under_budget')
    wip_account_id = fields.Many2one(comodel_name='account.account', string='WIP Account')
    wip_net = fields.Float(string='WIP Net', compute='compute_wip_net')
    wip_variance = fields.Float(string='WIP Variance', compute='compute_wip_variance')
    wip_variance_percentage = fields.Char(string='WIP Variance Percentage', compute='compute_wip_variance_percentage')
    wip_over_under_budget = fields.Selection(string='Over/Under Budget (WIP)',
                                             selection=[('under', 'Under Budget'),
                                                        ('equal', 'Equal Budget'),
                                                        ('over', 'Over Budget')],
                                             compute='compute_wip_over_under_budget')

    # Methods
    @api.depends('account_id', 'job_card_id.actual_line_calc')
    def compute_actual_net(self):
        for rec in self:
            actual_net = 0
            for actual_line_calc in rec.job_card_id.actual_line_calc:
                if rec.account_id == actual_line_calc.account_id:
                    actual_net += actual_line_calc.debit - actual_line_calc.credit
            rec.actual_net = actual_net

    @api.depends('wip_account_id', 'job_card_id.actual_line_calc')
    def compute_wip_net(self):
        for rec in self:
            wip_net = 0
            for actual_line_calc in rec.job_card_id.actual_line_calc:
                if rec.wip_account_id == actual_line_calc.account_id:
                    wip_net += actual_line_calc.debit - actual_line_calc.credit
            rec.wip_net = wip_net

    @api.depends('cost', 'actual_net')
    def compute_variance(self):
        for rec in self:
            rec.variance = rec.cost - rec.actual_net

    @api.depends('cost', 'wip_net')
    def compute_wip_variance(self):
        for rec in self:
            rec.wip_variance = rec.cost - rec.wip_net

    @api.depends('cost', 'variance')
    def compute_variance_percentage(self):
        for rec in self:
            if rec.cost:
                rec.variance_percentage = str(round(((rec.variance / rec.cost) * 100), 2)) + '%'
            else:
                rec.variance_percentage = False

    @api.depends('cost', 'wip_variance')
    def compute_wip_variance_percentage(self):
        for rec in self:
            if rec.cost:
                rec.wip_variance_percentage = str(round(((rec.wip_variance / rec.cost) * 100), 2)) + '%'
            else:
                rec.wip_variance_percentage = False

    @api.depends('variance')
    def compute_over_under_budget(self):
        for rec in self:
            if rec.variance < 0:
                rec.over_under_budget = 'over'
            elif rec.variance == 0:
                rec.over_under_budget = 'equal'
            else:
                rec.over_under_budget = 'under'

    @api.depends('wip_variance')
    def compute_wip_over_under_budget(self):
        for rec in self:
            if rec.wip_variance < 0:
                rec.wip_over_under_budget = 'over'
            elif rec.wip_variance == 0:
                rec.wip_over_under_budget = 'equal'
            else:
                rec.wip_over_under_budget = 'under'


class ActualLine(models.Model):
    _name = 'actual.line'
    _description = 'Actual Lines'
    _rec_name = 'account_id'

    # Fields
    job_card_id = fields.Many2one(comodel_name='job.card')
    account_id = fields.Many2one(comodel_name='account.account', string='Account', required=True)
    debit = fields.Float(string='DR')
    credit = fields.Float(string='CR')
    net = fields.Float(string='Net')


class ActualLineCalc(models.Model):
    _name = 'actual.line.calc'
    _description = 'Actual Lines (For Calculations)'
    _rec_name = 'account_id'

    # Fields
    job_card_id = fields.Many2one(comodel_name='job.card')
    account_id = fields.Many2one(comodel_name='account.account', string='Account', required=True)
    debit = fields.Float(string='DR')
    credit = fields.Float(string='CR')
    net = fields.Float(string='Net')


class BudgetWipLine(models.Model):
    _name = 'budget.wip.line'
    _description = 'WIP'
    _rec_name = 'item_id'

    # Fields
    job_card_id = fields.Many2one(comodel_name='job.card')
    name = fields.Char(string=' ')
    display_type = fields.Selection([
        ('line_section', 'Section'),
        ('line_note', 'Note'),
    ], default=False, help="Technical field for UX purpose.")
    item_id = fields.Many2one(comodel_name='product.template', string='Item')
    quantity = fields.Float(string='Quantity')
    unit_cost = fields.Float(string='Unit Cost')
    cost = fields.Float(string='Budget')
    account_id = fields.Many2one(comodel_name='account.account', string='Actual Account')
    actual_net = fields.Float(string='Actual Net', compute='compute_actual_net')
    wip_account_id = fields.Many2one(comodel_name='account.account', string='WIP Account')
    debit = fields.Float(string='DR', compute='compute_debit')
    credit = fields.Float(string='CR', compute='compute_credit')
    wip_net = fields.Float(string='WIP Net', compute='compute_wip_net')
    wip_variance = fields.Float(string='WIP Variance', compute='compute_wip_variance')
    wip_over_under_budget = fields.Selection(string='Over/Under Budget (WIP)',
                                             selection=[('under', 'Under Budget'),
                                                        ('equal', 'Equal Budget'),
                                                        ('over', 'Over Budget')],
                                             compute='compute_wip_over_under_budget')

    # Methods
    @api.depends('account_id', 'job_card_id.actual_line_calc')
    def compute_actual_net(self):
        for rec in self:
            actual_net = 0
            for actual_line_calc in rec.job_card_id.actual_line_calc:
                if rec.account_id == actual_line_calc.account_id:
                    actual_net += actual_line_calc.debit - actual_line_calc.credit
            rec.actual_net = actual_net

    @api.depends('wip_account_id', 'job_card_id.actual_line_calc')
    def compute_debit(self):
        for rec in self:
            debit = 0
            for actual_line_calc in rec.job_card_id.actual_line_calc:
                if rec.wip_account_id == actual_line_calc.account_id:
                    debit += actual_line_calc.debit
            rec.debit = debit

    @api.depends('wip_account_id', 'job_card_id.actual_line_calc')
    def compute_credit(self):
        for rec in self:
            credit = 0
            for actual_line_calc in rec.job_card_id.actual_line_calc:
                if rec.wip_account_id == actual_line_calc.account_id:
                    credit += actual_line_calc.credit
            rec.credit = credit

    @api.depends('wip_account_id', 'job_card_id.actual_line_calc')
    def compute_wip_net(self):
        for rec in self:
            wip_net = 0
            for actual_line_calc in rec.job_card_id.actual_line_calc:
                if rec.wip_account_id == actual_line_calc.account_id:
                    wip_net += actual_line_calc.debit - actual_line_calc.credit
            rec.wip_net = wip_net

    @api.depends('cost', 'debit')
    def compute_wip_variance(self):
        for rec in self:
            rec.wip_variance = rec.cost - rec.debit

    @api.depends('wip_variance')
    def compute_wip_over_under_budget(self):
        for rec in self:
            if rec.wip_variance < 0:
                rec.wip_over_under_budget = 'over'
            elif rec.wip_variance == 0:
                rec.wip_over_under_budget = 'equal'
            else:
                rec.wip_over_under_budget = 'under'
