# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class CostEstimationQuotationiNH(models.Model):
    _inherit = 'sale.order'
    # budget = fields.Many2one('crossovered.budget',string="Budget", readonly=True)

