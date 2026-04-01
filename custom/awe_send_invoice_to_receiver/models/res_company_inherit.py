# -*- coding: utf-8 -*-

from odoo import models, fields, api


class res_company_inherit(models.Model):
    _inherit = 'res.company'

    e_invoice = fields.Boolean('E-Invoice')
