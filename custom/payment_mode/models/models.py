# -*- coding: utf-8 -*-

from odoo import models, fields, api

class payment_mode(models.Model):
    _inherit = 'hr.expense'

    payment_method = fields.Selection([
        ("cash", "Cash"),
        ("credit", "Credit Card")
    ],
        states={'done': [('readonly', True)], 'post': [('readonly', True)], 'submitted': [('readonly', True)]}, string="Payment Method")


    credit_owner = fields.Char(string="owner")

    holidays_id = fields.Many2one(
        comodel_name='hr.leave',
        string='Holidays_id',
        required=False)