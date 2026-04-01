# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ReClass(models.Model):
    _inherit = 'purchase.order'

    requisitioner = fields.Many2one(comodel_name="res.users", string="Requisitioner", required=False, readonly=False,
                                    default=lambda self: self.create_uid)

    re_email = fields.Char(string="E-mail", required=False, related='requisitioner.partner_id.email')

    re_department = fields.Many2one(comodel_name="crm.team", string="Department", required=False, )
    payment_method = fields.Selection(string="", selection=[('bank', 'Bank Transfer'), ('cash', 'Cash'), ],
                                      required=False, )

    @api.model
    def create(self, values):
        result = super(ReClass, self).create(values)
        result.requisitioner = result.create_uid.id
        return result
