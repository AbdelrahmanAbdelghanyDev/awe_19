# -*- coding: utf-8 -*-

from odoo import models, fields, api

class projectTask(models.Model):
    _inherit = 'project.task'

    stage_id_name = fields.Char(
        string='Stage_id_name', 
        required=False)
