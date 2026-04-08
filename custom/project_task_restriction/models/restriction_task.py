from odoo import api, fields, models

class Rest_on_task(models.Model):
    _inherit='project.task.type'

    allowed_user_ids = fields.Many2many('res.users', string='Allowed Users')
