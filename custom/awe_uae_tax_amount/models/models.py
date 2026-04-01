# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    is_uae = fields.Boolean(compute='_compute_is_uae')

    @api.depends('company_id')
    def _compute_is_uae(self):
        for rec in self:
            if rec.company_id.id == 5:
                rec.is_uae = True
            else:
                rec.is_uae = False

    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #
    #     if self.env.company.id == 5:
    #         from lxml import etree
    #         doc = etree.XML(res['arch'])
    #         for node in doc.xpath("//field[@name='tax_ids']"):
    #             node.set('string', 'Rate')
    #         res['arch'] = etree.tostring(doc, encoding='unicode')
    #     return res


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    tax_amount = fields.Float(string='Tax Amount', compute='compute_tax_amount')

    @api.depends('price_subtotal', 'tax_ids')
    def compute_tax_amount(self):
        for rec in self:
            rec.tax_amount = rec.price_subtotal * (rec.tax_ids.amount / 100)

    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields=allfields, attributes=attributes)
        if self.env.company.id == 5 and 'tax_ids' in res:
            res['tax_ids']['string'] = "Rate"
        return res
