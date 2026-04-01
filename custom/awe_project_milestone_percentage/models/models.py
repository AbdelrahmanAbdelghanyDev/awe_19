# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_type_2 = fields.Selection(string="Project Type", selection=[('adhoc', 'Adhoc'),
                                                                        ('tracker', 'Tracker'),
                                                                        ('waves', 'Waves'),
                                                                        ('syndicated', 'Syndicated')],
                                      required=False)


class ADHOCProjectMilestoneSettingsLine(models.Model):
    _name = 'adhoc.project.milestone.setting.line'
    _description = 'ADHOC Project Milestone Settings Line'

    setting_id = fields.Many2one(comodel_name="project.milestone.setting")
    task_type_stage_id = fields.Many2one('project.task.type', required=True, string='Stage')
    percentage = fields.Float(string="Percentage %", default=0.0)
    sequence = fields.Integer(string="Sequence")


class OtherProjectMilestoneSettingsLine(models.Model):
    _name = 'other.project.milestone.setting.line'
    _description = 'Other Project Milestone Settings Line'

    setting_id = fields.Many2one(comodel_name="project.milestone.setting")
    task_type_stage_id = fields.Many2one('project.task.type', required=True, string='Stage')
    percentage = fields.Float(string="Percentage %", default=0.0)
    sequence = fields.Integer(string="Sequence")


class ProjectMilestoneSettings(models.Model):
    _name = 'project.milestone.setting'
    _rec_name = 'name'
    _description = 'Project Milestone Settings'

    name = fields.Char(string="Name")
    adhoc_line_ids = fields.One2many(comodel_name="adhoc.project.milestone.setting.line", inverse_name="setting_id",
                                     string="ADHOC Milestones")
    other_line_ids = fields.One2many(comodel_name="other.project.milestone.setting.line",
                                     inverse_name="setting_id", string="Other Milestones")

    @api.constrains('other_line_ids')
    def other_milestones_constrains(self):
        for rec in self:
            if rec.other_line_ids:
                if sum(rec.other_line_ids.mapped('percentage')) != 100:
                    raise ValidationError('The Sum of Other milestones\' percentages not equal 100')

    @api.constrains('adhoc_line_ids')
    def adhoc_milestones_constrains(self):
        for rec in self:
            if rec.adhoc_line_ids:
                if sum(rec.adhoc_line_ids.mapped('percentage')) != 100:
                    raise ValidationError('The Sum of ADHOC milestones\' percentages not equal 100')


class ProjectMilestoneLine(models.Model):
    _name = 'project.milestone.line'
    _description = 'Project Milestone Line'

    task_type_stage_id = fields.Many2one('project.task.type', required=True, string='Stage')
    task_id = fields.Many2one(comodel_name="project.task", string="Task")
    percentage = fields.Float(string="Percentage %")
    planned_revenue = fields.Float(string="Planned Revenue", compute='_get_milestone_parameters', store=True)
    poc_date = fields.Date(string="POC T.M.O.C")
    margin_after_travel = fields.Float('Margin', compute='_get_milestone_parameters')
    planned_cost = fields.Float(string="Planned GM", compute='_get_milestone_parameters', store=True)
    account_move_id = fields.Many2one(comodel_name="account.move", string="Journal Entry")
    project_id = fields.Many2one(comodel_name="project.project", string="Project",
                                 related='task_id.project_id', store=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner",
                                 related='task_id.partner_id', store=True)
    sales_bu = fields.Many2one(comodel_name="crm.team", string="Sales BU",
                               related='task_id.Sales_bu', store=True)
    project_type = fields.Selection(string="Project Type", related='task_id.project_type', store=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company",
                                 related='task_id.company_id', store=True)

    revenue_team_id = fields.Many2one(comodel_name="revenue.team", string="Revenue Team",
                                      related='task_id.Revenue_bu', store=True)

    @api.depends('task_id.converted_revenue',
                 'percentage',
                 'task_id.project_id.sale_order_id.budget_total',
                 'task_id.project_id.sale_order_id.budget_total_x',
                 'task_id.project_id.sale_order_id.amount_untaxed')
    def _get_milestone_parameters(self):
        for rec in self:
            # sale_order_id = rec.task_id.project_id.sale_order_id
            sale_order_id = rec.task_id.sale_order_id
            amount_untaxed = sale_order_id.amount_untaxed
            margin_percentage_after = 0
            if sale_order_id.budget_total >= 0:
                margin_percentage_after = (sale_order_id.margin_after_travel / amount_untaxed) if amount_untaxed != 0 else 0
            if sale_order_id.budget_total_x > 0 and sale_order_id.budget_total == 0:
                margin_percentage_after = (sale_order_id.margin_after_travel_x / amount_untaxed) if amount_untaxed != 0 else 0
            if sale_order_id.amount_untaxed < 0 :
                margin_percentage_after = (sale_order_id.x_studio_original_pr.margin_after_travel_x / sale_order_id.x_studio_original_pr.amount_untaxed ) if sale_order_id.x_studio_original_pr.amount_untaxed != 0 else 0
            rec.margin_after_travel = margin_percentage_after * 100
            rec.planned_revenue = (rec.percentage / 100) * rec.task_id.converted_revenue
            rec.planned_cost = rec.planned_revenue * margin_percentage_after


class Task(models.Model):
    _inherit = 'project.task'

    project_type = fields.Selection(string="Project Type", selection=[('adhoc', 'Adhoc'),
                                                                      ('tracker', 'Tracker'),
                                                                      ('waves', 'Waves'),
                                                                      ('syndicated', 'Syndicated')],
                                    related='project_id.sale_order_id.project_type_2')

    milestone_ids = fields.One2many(comodel_name="project.milestone.line", inverse_name="task_id",
                                    string="Milestones")

    def stage_revenue(self):
        self.ensure_one()
        # milestone_line = self.milestone_ids.search([('task_type_stage_id', '=', self.stage_id.id)], limit=1)
        milestone_line = self.milestone_ids.filtered(lambda l: l.task_type_stage_id == self.stage_id)
        if not milestone_line.poc_date:
            raise ValidationError('Please insert POC Date for line %s' % milestone_line.task_type_stage_id.name)
        if milestone_line.account_move_id:
            raise ValidationError('Journal Entry for this stage has already created')
        converted_revenue = milestone_line.planned_revenue
        project_revenue_accounts = self.env['revenue_accounts']
        journal_entry_item = self.env['account.move.line']
        journal_entry = self.env['account.move']
        p_r_accounts = project_revenue_accounts.search(
            [('tag', '=', self.tag_id.id), ('company_id', '=', self.company_id.id)])

        current_company_id = self.company_id.id
        journal = self.env['account.journal'].search(
            [('code', '=', 'PR.C.'), ('company_id', '=', current_company_id)])

        if not p_r_accounts:
            if self.tag_id.name:
                message = (
                        'Can\'t Create Journal Entry!\n' + 'Please Create Revenue account with the tag: ' +
                        self.tag_id.name)
            else:
                message = ('Can\'t Create Journal Entry!\n' + 'No tag found ')
            raise ValidationError(message)

        current_company_id = self.company_id.id
        journal = self.env['account.journal'].search(
            [('code', '=', 'PR.C.'), ('company_id', '=', current_company_id)])
        if p_r_accounts:
            journal_entry_id = journal_entry.create({
                'date': self.date_deadline,  # fields.Date.today(),
                'journal_id': journal.id,
                'ref': self.project_id.name,
                # 'name': 'Project Completion ' + self.project_id.analytic_account_id.display_name,
                'name': self.env['ir.sequence'].search(
                    [('name', '=', 'Project Closure'), ('company_id', '=', self.company_id.id)]).next_by_id(),
                'cor': '(revenue)'
            })
            journal_entry_item.with_context(check_move_validity=False).create({
                'account_id': p_r_accounts.accrued_acc_id.id,
                'analytic_account_id': self.project_id.analytic_account_id.id,
                # 'analytic_tag_ids': self.Revenue_bu.analytic_tag_ids.ids,
                'move_id': journal_entry_id.id,
                # 'debit': converted_revenue,
                'debit': self.original_currency_id.compute(self.revenue * (milestone_line.percentage/100),
                                                           self.env.company.currency_id),
                'amount_currency': self.revenue * (milestone_line.percentage/100),
                # 'amount_currency': self.revenue,
                'currency_id': self.original_currency_id.id,
            })
            journal_entry_item.with_context(check_move_validity=False).create({
                'account_id': p_r_accounts.revenue_acc_id.id,
                'analytic_account_id': self.project_id.analytic_account_id.id,
                # 'analytic_tag_ids': self.Revenue_bu.analytic_tag_ids.ids,
                'move_id': journal_entry_id.id,
                'credit': self.original_currency_id.compute(self.revenue * (milestone_line.percentage/100),
                                                            self.env.company.currency_id),
                'amount_currency': -self.revenue * (milestone_line.percentage/100),
                # 'amount_currency': -self.revenue,
                'currency_id': self.original_currency_id.id,
            })

            self.is_revenue_button_clicked = True

            self.env['account.move'].search([('invoice_origin', '=', self.sale_line_id.order_id.name)]).write({
                'is_revenue_button_clicked': self.is_revenue_button_clicked,
                'task_state': self.stage_id.id})

            milestone_line.update({
                'account_move_id': journal_entry_id.id
            })

    def create_project_milestones(self):
        for rec in self:
            project_type = rec.project_type
            setting = self.env.ref('awe_project_milestone_percentage.project_milestone_setting_record')
            milestones = []
            if project_type == 'adhoc':
                for line in setting.adhoc_line_ids:
                    milestones.append((0, 0, {
                        'task_type_stage_id': line.task_type_stage_id.id,
                        'percentage': line.percentage
                    }))
            else:
                for line in setting.other_line_ids:
                    milestones.append((0, 0, {
                        'task_type_stage_id': line.task_type_stage_id.id,
                        'percentage': line.percentage
                    }))
            rec.milestone_ids = milestones

    @api.model
    def create(self, vals):
        if 'sale_order_id' in vals:
            project_type = self.env['sale.order'].browse(vals.get('sale_order_id')).project_type_2
            setting = self.env.ref('awe_project_milestone_percentage.project_milestone_setting_record')
            milestones = []
            if project_type == 'adhoc':
                for line in setting.adhoc_line_ids:
                    milestones.append((0, 0, {
                        'task_type_stage_id': line.task_type_stage_id.id,
                        'percentage': line.percentage
                    }))
            else:
                for line in setting.other_line_ids:
                    milestones.append((0, 0, {
                        'task_type_stage_id': line.task_type_stage_id.id,
                        'percentage': line.percentage
                    }))
            vals['milestone_ids'] = milestones
        return super(Task, self).create(vals)


class RevenueTeam(models.Model):
    _inherit = 'revenue.team'

    # analytic_tag_ids = fields.Many2many(comodel_name="account.analytic.tag", string="Analytic Tags")







