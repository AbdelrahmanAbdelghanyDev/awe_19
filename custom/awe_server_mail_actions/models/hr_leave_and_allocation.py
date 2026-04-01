# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class HrHolidays(models.Model):
#     _inherit = 'hr.holidays'
#
#     def approve_server_Action(self):
#         for rec in self:
#             if rec.state in ['draft','confirm']:
#                 rec.state = 'validate'
#                 # rec.write({
#                 #     'state' : 'validate'
#                 # })