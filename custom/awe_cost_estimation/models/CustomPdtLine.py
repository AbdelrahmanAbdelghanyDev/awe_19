# -*- coding: utf-8 -*-

from odoo import models, fields, api

SEC = [
    ('A', 'A'),
    ('AB', 'AB'),
    ('BC1', 'BC1'),
    ('C1', 'C1'),
    ('C2', 'C2'),
    ('C1C2', 'C1C2'),
    ('C2D', 'C2D'),
    ('D', 'D'),
    ('E', 'E'),
    ('DE', 'DE'),
]



class CustomPdtLine(models.Model):
    _inherit = 'crm.product_line'

    research_type_id = fields.Char(
        # 'product.category',
        required=False,
        # related='pdt_crm.research_type_id.name',
        # default=lambda self: self.pdt_crm.research_type_id.name,
        # compute='compute_category',
        # store=True

    )

    # @api.model
    # def test(self):
    #     catg = self.pdt_crm.research_type_id.id
    #     self.write({'research_type_id': catg})
    #     return True
    # @api.onchange

    #
    # @api.onchange('research_type_id')
    # def compute_category(self):
    #     print('::: compute_category :::')
    #     catg = self.pdt_crm.research_type_id.id
    #     self.write({'research_type_id': catg})
    #     print('::: out :::')
    #     return True

    #
    # @api.onchange('product_id')
    # def get_domain_ids(self):
    #     print (':::get_domain_ids ::::')
    #     # try:
    #     #     return {
    #     #         'domain': {
    #     #             'product_id': [
    #     #                 ('categ_id', '=', self._context['product_category_id']),
    #     #                 ('sale_ok', '=', True)
    #     #             ]
    #     #         }
    #     #     }
    #     # except Exception:
    #     #     print('IAm Excepted')
    #     #     return {}
    #     # print('::: compute_category :::')
    #     catg = self.pdt_crm.research_type_id.id
    #     self.write({'research_type_id': catg})
    #     return True



