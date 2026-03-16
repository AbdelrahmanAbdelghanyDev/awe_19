# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Sector(models.Model):
    _name = 'sector'

    name = fields.Char(string='Name')

#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class CustomLead(models.Model):
    _inherit = 'crm.lead'

    planned_revenue = fields.Float(string='Expected Sales')
    sector_id = fields.Many2one('sector', 'Sector')
    sales_country_id = fields.Many2one('res.country', 'Sales Country')
    lead_country_id = fields.Many2one('res.country', 'Lead Country')
    invoice_country_id = fields.Many2one('res.country', 'Invoice Country')
    work_country_id = fields.Many2one('res.country', 'Work Country')


class CustomPartner(models.Model):

    _inherit = 'res.partner'

    sector_id = fields.Many2one('sector', 'Sector')

