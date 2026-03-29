# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# MONTHES = [
#     ('january', 'January'),
#     ('february', 'February'),
#     ('march', 'March'),
#     ('april', 'April'),
#     ('may', 'May'),
#     ('june', 'June'),
#     ('july', 'July'),
#     ('august', 'August'),
#     ('september', 'September'),
#     ('october', 'October'),
#     ('november', 'November'),
#     ('december', 'December'),
# ]

# class Task(models.Model):
#     _inherit = "project.task"
#
#     planned_hours = fields.Float(string='Sample Size', help='Estimated time to do the task, usually set by the project manager when the task is in draft state.')

class add_revenue_crm_lead(models.Model):
    _inherit = 'crm.lead'

    revenue_bu = fields.Many2one('revenue.team', string="Revenue BU" ,required=True)


class CustomProject(models.Model):
    _name = 'project.project'
    _inherit = ['project.project']

    mon = fields.Date(string='Month of Completion ',required=True)
    internl_pro_name = fields.Char(string='Internal Project Name')


class ProductImage(models.Model):
    _inherit = 'project.task'

    img_name = fields.Char(string="Alternative text",
                           required=True, translate=True)

    task_id = fields.Many2one(
        'project.task', string='Task', ondelete='set null', index=True)

    team_id = fields.Many2one('project.task.teams', 'Team')

    original_image = fields.Binary(string='Original image')

    medium_image = fields.Binary(
        string='Medium image', compute='_resize_image', store=True)

    small_image = fields.Binary(
        string='Small image', compute='_resize_image', store=True)

    date_start_splited = fields.Date(
        string='Start Date2', compute='_split_date', store=True)

    date_end_splited = fields.Date(
        string='End Date2', compute='_split_date', store=True)

    time_start = fields.Char(
        string='Start Time', compute='_split_date', store=True)

    time_end = fields.Char(
        string='End Time', compute='_split_date', store=True)

    traveling_time = fields.Datetime('Target(month of completion)',required=True ,tracking=True)#'Traveling Time'

    today_date = fields.Date(
        'Today',
        readonly=True,
        default=lambda self: fields.Datetime.now()
    )
    today_flag = fields.Boolean('Today Flag',
                                default=False,
                                compute='_split_date',
                                store=True
                                )
    executive_person = fields.Many2one('executive.team', string="Executive Person")
    Revenue_bu = fields.Many2one('revenue.team', string="Revenue BU",tracking=True)
    Sales_bu = fields.Many2one('crm.team', string="Sales BU",tracking=True)
    date_end1 = fields.Datetime(string='Ending Date', index=True, copy=False)

    user_check = fields.Boolean(compute="_check_group")

    @api.depends('name')
    def _check_group(self):
        print('x',self)
        groups_list = []
        self.user_check = False
        for rec in self.env.user.groups_id:
            groups_list.append(rec.name)
        print('groups_list',groups_list)
        if "Finance Team" not in groups_list:
            print('eee',self.active)
            return False
        else:
            print('bbb',self)
            self.user_check = True

    @api.constrains('active')
    def onch_active(self):
        groups_list = []
        for rec in self.env.user.groups_id:
            groups_list.append(rec.name)
        print('groups_list',groups_list)
        for line in self:
            if "Finance Team" not in groups_list and (line.active == False):
                raise UserError(_('You have no Access to Archive task'))
    # temp2_ids = fields.One2many('project.task','project_id',string='Filtered Tasks')
    # temp_ids = fields.Integer(
    #     string='Filtered Tasks',
    #     compute='_get_ids',
    #     store=True
    # )

    # ids = self.search([('date_start', '>', today_date),
    #                    ('date_end', '<', today_date)])

    #
    # def _get_ids(self):
    #     _logger.error('########qweweqw IAM IN ##########')
    #     ids = self.search([
    #         ('date_start', '>', self.today_date),
    #         ('date_end', '<', self.today_date)
    #     ])
    #     # _logger.error(ids)
    #     if ids:
    #         self.temp_ids = ids
    #     _logger.error(self.temp_ids)


    @api.depends('date_end1')
    def _set_date_end(self):
        if self.date_end1:
            self.date_end = self.date_end1


    @api.depends( 'date_end1')
    def _split_date(self):
            # date_start = self.with_context({}).date_start
            # date_end = self.with_context({}).date_end
        for rec in self:
            if rec.date_end1:
                rec.date_end_splited = rec.date_end1.split(' ')[0]
                rec.time_end = rec.date_end1.split(' ')[1]
            if rec.date_start_splited and rec.date_end_splited:
                if rec.date_start_splited < rec.today_date and rec.date_end_splited > rec.today_date:
                    rec.today_flag = True
            else:
                rec.date_start_splited = False
                rec.time_start = False


    @api.depends('original_image')
    def _resize_image(self):
        for rec in self:
            original_image = rec.with_context({}).original_image
            if original_image:
                data = tools.image_get_resized_images(original_image)
                rec.medium_image = data['image_medium']
                rec.small_image = data['image_small']
            else:
                rec.medium_image = ""
                rec.small_image = ""


class Teams(models.Model):
    _name = 'project.task.teams'
    _inherit = ['mail.thread']

    name = fields.Char("Team Name", required=True)

    member_ids = fields.One2many(
        'team.members',
        'team_id',
        string='Related Member',

    )


class TeamMembers(models.Model):
    _name = 'team.members'

    name = fields.Char("Member Name", required=True)
    team_id = fields.Many2one('project.task.teams', 'Team Member')


# class CustomRepair(models.Model):
#     _inherit = ['mrp.repair']
#
#     project_id = fields.Many2one('project.project', 'Project')


class ReportProjectTaskUser(models.Model):
    _inherit = "report.project.task.user"

    traveling_time = fields.Datetime('Target(month of completion)', readonly=True)

    def _select(self):
        return super(ReportProjectTaskUser, self)._select() + """,
            traveling_time as traveling_time"""

    def _group_by(self):
        return super(ReportProjectTaskUser, self)._group_by() + """,
            traveling_time"""

