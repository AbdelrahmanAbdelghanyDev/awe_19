# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_type_id = fields.Many2one('res.project.type')
    methodology_id = fields.Many2one('res.methodology')
