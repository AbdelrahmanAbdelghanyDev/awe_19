# -*- coding: utf-8 -*-

from odoo import models, fields, api



class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    is_project_manager = fields.Boolean('Is Project Manager')





class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    project_manager_id = fields.Many2one('res.users', string='Project Manager', required=True,domain=[('is_project_manager', '=', True)])

    def write(self, vals):
        res = super(SaleOrderInherit, self).write(vals)
        if 'project_manager_id' in vals:
            for record in self:
                for project in record.project_ids:
                    project.user_id = record.project_manager_id
        return res


class ProjectInherit(models.Model):
    _inherit = 'project.project'
    user_id = fields.Many2one('res.users', string='Project Manager' ,tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        self = self.with_context(mail_create_nosubscribe=True)

        for vals in vals_list:
            if 'sale_line_id' in vals:
                order_line = self.env['sale.order.line'].browse(vals['sale_line_id'])
                vals.write({
                    'user_id': order_line.order_id.project_manager_id.id
                })

        projects = super(ProjectInherit, self).create(vals_list)

        for project in projects:
            if project.privacy_visibility == 'portal' and project.partner_id:
                project.message_subscribe(project.partner_id.ids)

        return projects