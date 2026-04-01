# -*- coding: utf-8 -*-
from odoo import http

# class CustomBills(http.Controller):
#     @http.route('/custom_bills/custom_bills/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_bills/custom_bills/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_bills.listing', {
#             'root': '/custom_bills/custom_bills',
#             'objects': http.request.env['custom_bills.custom_bills'].search([]),
#         })

#     @http.route('/custom_bills/custom_bills/objects/<model("custom_bills.custom_bills"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_bills.object', {
#             'object': obj
#         })