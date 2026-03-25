# -*- coding: utf-8 -*-
from os import access

from odoo import models, fields, api

class ProductCanBeCost(models.Model):
    _inherit = "product.product"
    methodology_id = fields.Boolean(string="Methodology", default=False)



class ProductCanBeCost(models.Model):
    _inherit = "product.template"

    cost_ok = fields.Boolean(string='Can be Cost Item')
    is_true = fields.Boolean(string='is true?')


    cost_estimation = fields.One2many('cost.estimation.products','idx')
    cost_item_type = fields.Selection([('material', 'Material'),('labour', 'Labour'),('overhead', 'Overhead')], string="CI Type")
    budgetary_position = fields.Many2one('account.budget.post', string='Budgetary Position')
    methodology_id = fields.Boolean(string="Methodology", default=False)


class ProductCostEstimation(models.Model):
    _name = "cost.estimation.products"

    product_id = fields.Many2one('product.template', string='Product')
    description = fields.Text('Description', related='product_id.description_picking',store=True)
    qty = fields.Float('Quantity')
    uom = fields.Many2one('uom.uom', string='Unit of Measure')
    # cost_item_type = fields.Selection([('material', 'Material'),('labour', 'Labour'),('overhead', 'Overhead')], string="CI Type")
    cost_item_type = fields.Selection(related='product_id.cost_item_type',string="CI Type")
    idx = fields.Many2one('product.template')
    access_description=fields.Boolean(string='access',compute='_access_description_filed' )

    def _access_description_filed(self):
        for rec in self:
            if self.env.user.has_group('cost_estimation.group_cost_estimation_users'):
                rec.access_description = True
            else:
                rec.access_description = False


    @api.onchange('product_id')
    def _onch_proj(self):

        self.uom = self.product_id.uom_id.id