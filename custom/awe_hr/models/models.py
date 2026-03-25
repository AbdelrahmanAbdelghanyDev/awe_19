# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    manager_name = fields.Char(related="parent_id.name", string="Manager Name", store=True, related_sudo=True,
                               compute_sudo=True)
    coach_name = fields.Char(related="coach_id.name", string="Coach Name", store=True, related_sudo=True,
                             compute_sudo=True)

    resignation_date = fields.Date(
        string='Resignation Date', 
        required=False)
    
    reason = fields.Text(
        string="Reason",
        required=False)
