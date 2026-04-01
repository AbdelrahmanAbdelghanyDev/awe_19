# -*- coding: utf-8 -*-

from odoo import models, fields, api


class JournalEntries(models.Model):
    _inherit = 'account.move'

    def _set_unposted_status_action(self):
        for rec in self:
            rec.state = 'draft'
