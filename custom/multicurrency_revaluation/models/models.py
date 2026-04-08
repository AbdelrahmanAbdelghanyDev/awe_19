# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountRev(models.Model):
    _inherit = 'account.account'

    currency_revaluation = fields.Boolean(
        string="Allow Currency Revaluation",
        default=False,
    )