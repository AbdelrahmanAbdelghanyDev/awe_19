# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class HRHolidaysInh(models.Model):
    _inherit = 'hr.employee'

    def _compute_leaves_count(self):
        leaves = self.env['hr.holidays'].read_group([
            ('employee_id', '=', self.id),
            ('state', '=', 'validate'),
            ('holiday_status_id.active', '=', True)
        ], fields=['number_of_days', 'employee_id'], groupby=['employee_id'])
        mapping = dict([(leave['employee_id'][0], leave['number_of_days']) for leave in leaves])
        for employee in self:
            employee.leaves_count = mapping.get(employee.id)


    def get_employee_id(self):
        return {
            'name': _('Leaves'),
            'res_model': 'hr.holidays',
            'type': 'ir.actions.act_window',
            # 'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain':[
            ('employee_id', '=', self.id),
            ('state', '=', 'validate'),
            ('holiday_status_id.active', '=', True)]
        }



