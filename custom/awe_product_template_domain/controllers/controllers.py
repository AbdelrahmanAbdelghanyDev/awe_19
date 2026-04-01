# -*- coding: utf-8 -*-
from odoo import http

# class AweProductTemplateDomain(http.Controller):
#     @http.route('/awe_product_template_domain/awe_product_template_domain/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/awe_product_template_domain/awe_product_template_domain/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('awe_product_template_domain.listing', {
#             'root': '/awe_product_template_domain/awe_product_template_domain',
#             'objects': http.request.env['awe_product_template_domain.awe_product_template_domain'].search([]),
#         })

#     @http.route('/awe_product_template_domain/awe_product_template_domain/objects/<model("awe_product_template_domain.awe_product_template_domain"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('awe_product_template_domain.object', {
#             'object': obj
#         })