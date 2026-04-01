from odoo import models, fields, api


# class cost_estimation_inherit_company(models.Model):
#     _inherit = 'cost.estimation.template'
#
#     company_id = fields.Many2one(
#         'res.company',
#         'Company',)

# class CostEstimationLineinherit(models.Model):
#         _inherit = "cost.estimate.line"
#
#         product_id = fields.Many2one('product.product', 'Product', domain=lambda self:[('company_id','=', self.env.user.company_id.id)],required=True)
#
#         quote_id = fields.Many2one('cost.estimation.template')