# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrLeaveInh(models.Model):
    _inherit = 'hr.leave'

    travel_id = fields.Many2one(
        comodel_name='hr.leave',
        string=' holidays_id',
        required=False)
    travel_purpose = fields.Selection(
        [('management', 'Management'), ('bd', "BD"), ('project execution', "Project Execution")], default='management',
        string="Travel Purpose")
    source_country = fields.Many2one('res.country', string="Source Country")
    destination_country = fields.Many2one('res.country', string="Destination Country")
    required_visa = fields.Selection([('yes', "Yes"), ('no', "No")], default='yes')
    passport_expiry = fields.Date(string="My passport expiry date")
    hotel_in = fields.Date(string="Hotel check in")
    hotel_out = fields.Date(string="Hotel check out")
    bu_team = fields.Selection([('support', 'Support'), ('research', "Research"), ('management', "Management")],
                               default='support', string="BU Team")
    support_type = fields.Selection([('it', 'IT'), ('finance', "Finance"), ('operations', "Operations"), ('hr', "HR")],
                                    default='it', string="Support type")
    research_type = fields.Selection([('ql', 'QL'), ('qn', "QN"), ('bd', "BD"), ('fs', "FS"), ('hc', 'HC')],
                                     default='ql', string="Research type")

    project_id = fields.Many2one('project.project', string="Project")
    holidays_id = fields.Many2one('hr.leave', string="Leave Source")
    employee_id = fields.Many2one('hr.employee')
    memo = fields.Text(string='Additional travel details')
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('validate1', 'Second Approval'),
        ('validate', 'Approved')
    ], string='Status', readonly=True, tracking=True, copy=False)

class purchaseOrderInh(models.Model):
    _inherit = 'purchase.order'

    # holidays_id = fields.Char(
    #     string='Holidays_id',
    #     required=False)

    holidays_id = fields.Many2one(
        comodel_name='hr.leave',
        string=' holidays_id',
        required=False)


    travel_purpose = fields.Selection(
            [('management', 'Management'), ('bd', "BD"), ('project execution', "Project Execution")], default='management',
            string="Travel Purpose")
