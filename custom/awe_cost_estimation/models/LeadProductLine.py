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



class LeadProductLine(models.Model):
    _inherit = 'crm.product_line'

    breif = fields.Char()
    fw_country = fields.Many2one('res.country.state')
    project_objective = fields.Many2one('project.objective')
    research_type = fields.Selection([('ql', 'QL'),
                                      ('qn', 'QN')])
    data_capture = fields.Selection([('capi', 'CAPI'),
                                     ('papi', 'PAPI'), ('cati', 'CATI'), ('online', 'Online')])
    # sample_size = fields.Many2one('sample.size')
    sample_size = fields.Char('SS')
    number_of_legs = fields.Integer()
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ('both', 'Both')])
    sec = fields.Selection(SEC)
    # fw_country = fields.Many2one('res.country', ' Country')
    fw_city_country = fields.Many2one('res.country', ' Country')
    age = fields.Char('Age')
    client_attendance = fields.Selection([('yes', 'Yes'),
                                          ('no', 'No')])
    no_of_respondants = fields.Integer('No of Respondants')
    no_of_attendees = fields.Integer('No of attendees')
    no_of_units_attendees = fields.Char('Number of Units')

    name = fields.Char(compute='_compute_name', string="Description")
    pdt_crm_research_id = fields.Char(related='pdt_crm.research_type_id.name')
    pdt_crm_2_research_id = fields.Char(related='pdt_crm_2.research_type_id.name', default='QL')

    # @api.onchange('pdt_line')
    # def get_domain_ids(self):
    #     print (':::get_domain_ids ::::')
    # print({
    #     'domain': {
    #         'product_id': [
    #             ('categ_id', '=', self._context['product_category_id'])
    #         ]
    #     }
    # })
    #     try:
    #         return {
    #             'domain': {
    #                 'product_id': [
    #                     ('categ_id', '=', self._context['product_category_id'])
    #                 ]
    #             }
    #         }
    #     except Exception:
    #         return []

    #
    @api.depends('product_id', 'fw_country', 'sec')
    def _compute_name(self):
        for record in self:
            record.name = ''
            if record.product_id:
                record.name += record.product_id.name + ', '
            if record.fw_country:
                record.name += record.fw_country.name + ', '
            if record.sec:
                record.name += record.sec

    # @api.onchange('product_id')
    # def product_domain(self):
    #     print(self._context)
    #     # products = self.env['product.product'].search([
    #     #     ('categ_id', '=', self._context['product_category_id']),
    #     #     # ('categ_id.parent_id', '=', self._context['product_category_id'])
    #     # ])
    #     products_2 = self.env['product.product'].search([
    #         # ('categ_id', '=', self._context['product_category_id']),
    #         ('categ_id.parent_id', '=', self._context['product_category_id']),
    #         ('purchase_ok', '=', True)
    #     ])
    #     # lst = products.ids
    #     # lst.append(products_2.ids)
    #     # print(products)
    #     return {'domain': {'product_id': [('id', 'in', products_2.ids)], }}
