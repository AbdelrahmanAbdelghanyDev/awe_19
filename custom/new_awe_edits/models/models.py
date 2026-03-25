# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessDenied


class new_awe_edits(models.Model):
    _inherit = 'sale.order'

    work_country_id = fields.Many2one('res.country', 'Work Country')
    work_country_id = fields.Many2one('res.country', 'Work Country')

    def write(self, values):
        if self.env.ref('custom_project.group_finance_team') not in self.env.user.groups_id:
            if 'third_party_cost' in values.keys():
                raise AccessDenied
        return super(new_awe_edits, self).write(values)

# class new_project_task(models.Model):
#     _inherit = 'project.task'
