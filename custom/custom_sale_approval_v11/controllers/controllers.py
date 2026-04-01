# -*- coding: utf-8 -*-
from odoo import http

# class CustomSaleApprovalV11(http.Controller):
#     @http.route('/custom_sale_approval_v11/custom_sale_approval_v11/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_sale_approval_v11/custom_sale_approval_v11/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_sale_approval_v11.listing', {
#             'root': '/custom_sale_approval_v11/custom_sale_approval_v11',
#             'objects': http.request.env['custom_sale_approval_v11.custom_sale_approval_v11'].search([]),
#         })

#     @http.route('/custom_sale_approval_v11/custom_sale_approval_v11/objects/<model("custom_sale_approval_v11.custom_sale_approval_v11"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_sale_approval_v11.object', {
#             'object': obj
#         })