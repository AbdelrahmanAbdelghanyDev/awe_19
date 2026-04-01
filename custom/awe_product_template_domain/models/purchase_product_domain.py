# from odoo import models, fields, api
#
#
# class CostEstimationLineinherit(models.Model):
#     _inherit = "purchase.order.line"
#
#     product_id = fields.Many2one('product.product', string='Product', domain=lambda self:[('purchase_ok', '=', True),('company_id', '=', self.env.user.company_id.id)],
#                                  change_default=True, required=True)
