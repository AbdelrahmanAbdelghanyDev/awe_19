# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import json


class RevenueBU(models.Model):
    _name = 'revenue.bu'
    _description = 'Job Card by Analytic Tag'
    _rec_name = 'analytic_account_id'

    # Fields
    analytic_account_id = fields.Many2one(comodel_name='account.analytic.account', string='Client',
                                          required=True)
    # analytic_tag_ids = fields.Many2many(comodel_name="account.analytic.tag", string="Analytic Tags")
    partner_id = fields.Many2one(comodel_name='res.partner', string='Customer',
                                 related='analytic_account_id.partner_id', store=True)
    # date_month = fields.Integer(store=True)
    # month_id = fields.Many2one(comodel_name='res.month', string='Month', store=True)
    revenue = fields.Float(string='Revenue')
    project_type_id = fields.Many2one(comodel_name='res.project.type', string='Project Type (Qn/QL)')
    project_type_2 = fields.Selection(string="Project Type (ATWS)", selection=[('adhoc', 'Adhoc'),
                                                                               ('tracker', 'Tracker'),
                                                                               ('waves', 'Waves'),
                                                                               ('syndicated', 'Syndicated')])
    revenue_cost = fields.Float(string='Cost of Revenue')
    gm = fields.Float(string='GM', compute='compute_gm', store=True)
    gm_percentage = fields.Char(string='GM Percentage', compute='compute_gm_percentage')

    # gm_percentage = fields.Char(string='GM Percentage', compute='compute_gm_percentage')

    # Methods
    # @api.depends('date_month')
    # def compute_month_id(self):
    #     for rec in self:
    #         rec.month_id = rec.env['res.month'].search([('num', '=', rec.date_month)], limit=1).id

    @api.depends('revenue', 'revenue_cost')
    def compute_gm(self):
        for rec in self:
            rec.gm = rec.revenue - rec.revenue_cost

    @api.depends('gm', 'revenue')
    def compute_gm_percentage(self):
        for rec in self:
            if rec.revenue:
                rec.gm_percentage = str(round(((rec.gm / rec.revenue) * 100), 2)) + '%'
            else:
                rec.gm_percentage = str(round(0, 2)) + '%'
            # if rec.revenue:
            #     rec.gm_percentage = round(((rec.gm / rec.revenue) * 100), 2)
            # else:
            #     rec.gm_percentage = 0
