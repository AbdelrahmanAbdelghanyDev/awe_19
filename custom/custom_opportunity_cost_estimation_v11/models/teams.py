# -*- coding: utf-8 -*-

from odoo import models, fields, api

SEC = [
    ('A', 'A'),
    ('AB', 'AB'),
    ('BC1', 'BC1'),
    ('C1', 'C1'),
    ('C2', 'C2'),
    ('C1C2', 'C1C2'),
    ('C2D', 'C2D'),
    ('D', 'D'),
    ('E', 'E'),
    ('DE', 'DE'),
]


class ExecutiveTeams(models.Model):
    _name = 'executive.team'
    _inherit = 'crm.team'

    def _get_default_favorite_user_ids(self):
        return [(6, 0, [self.env.uid])]

    favorite_user_ids = fields.Many2many(
        'res.users', 'executive_team_favorite_user_rel', 'executive_team_id', 'user_id',
        default=_get_default_favorite_user_ids,
        string='Members')

    # member_ids = fields.One2many('hr.employee', 'sale_employee_id', string='Channel Members')

    # member_ids = fields.One2many('res.users', 'sale_team_id', string='Executive Team')


class RevenueTeams(models.Model):
    _name = 'revenue.team'
    _inherit = 'crm.team'

    def _get_default_favorite_user_ids(self):
        return [(6, 0, [self.env.uid])]

    favorite_user_ids = fields.Many2many(
        'res.users', 'revenue_team_favorite_user_rel', 'revenue_team_id', 'user_id',
        default=_get_default_favorite_user_ids,
        string='Members')
    # member_ids = fields.One2many('hr.employee', 'sale_employee_id', string='Channel Members')

