from odoo import models, fields, api


class CostEstimationLineinherit(models.Model):
    _inherit = "sale.order.line"

    product_id = fields.Many2one('product.product', string='Product',
                                 domain=lambda self: [('sale_ok', '=', True),
                                                      ('company_id', '=', self.env.user.company_id.id)],
                                 change_default=True, ondelete='restrict', required=True)
