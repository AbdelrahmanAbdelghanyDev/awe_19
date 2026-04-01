# -*- coding: utf-8 -*-
from odoo import http

# class CustomSalesContext(http.Controller):
#     @http.route('/custom_sales_context/custom_sales_context/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_sales_context/custom_sales_context/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_sales_context.listing', {
#             'root': '/custom_sales_context/custom_sales_context',
#             'objects': http.request.env['custom_sales_context.custom_sales_context'].search([]),
#         })

#     @http.route('/custom_sales_context/custom_sales_context/objects/<model("custom_sales_context.custom_sales_context"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_sales_context.object', {
#             'object': obj
#         })