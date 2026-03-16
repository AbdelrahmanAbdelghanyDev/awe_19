# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrderInh(models.Model):
    _inherit = 'sale.order'

    check_confirmation_group_date = fields.Datetime(string='Confirmation Date')

    check_confirmation_group = fields.Boolean(
        string='Check Confirmation Group',
        compute='_compute_check_confirmation_group',
        store=True
    )

    def _compute_check_confirmation_group(self):
        for rec in self:
            rec.check_confirmation_group = self.env.user.has_group(
                'awe_confirmation_date_group.confirmation_date_editable_group'
            )

    def action_confirm(self):
        res = super(SaleOrderInh, self).action_confirm()

        if self.env.user.has_group('awe_confirmation_date_group.confirmation_date_editable_group'):
            self.check_confirmation_group = False
            self.confirmation_date = self.check_confirmation_group_date
        else:
            self.check_confirmation_group = False

        return res