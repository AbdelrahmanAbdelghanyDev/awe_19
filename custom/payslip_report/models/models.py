# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Employees(models.Model):
    _inherit = 'hr.employee'

    bank_id = fields.Char('Bank ID')
    branch = fields.Char('Branch')
