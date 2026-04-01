# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomPivot(models.Model):
    _inherit = 'sale.order'

    margin_after_travel = fields.Float(compute='_compute_margin', store=True, string="CP After Travel")
    budget_total = fields.Float(compute='_compute_budget_total', store=True)
    budget_total_x = fields.Float(compute='_compute_budget_total_x', store=True, string="Cost (budget currency)")

