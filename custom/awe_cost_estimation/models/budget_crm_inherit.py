from odoo import models, fields, api

class mak_domain_order_line(models.Model):
    _inherit = 'custom.sale.order.line'

    budget_crm_research_id = fields.Char(related='parent_cost.estimation_type.name')
