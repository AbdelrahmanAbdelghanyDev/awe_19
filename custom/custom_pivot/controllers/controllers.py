# -*- coding: utf-8 -*-
from odoo import http

# class CustomPivot(http.Controller):
#     @http.route('/custom_pivot/custom_pivot/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_pivot/custom_pivot/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_pivot.listing', {
#             'root': '/custom_pivot/custom_pivot',
#             'objects': http.request.env['custom_pivot.custom_pivot'].search([]),
#         })

#     @http.route('/custom_pivot/custom_pivot/objects/<model("custom_pivot.custom_pivot"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_pivot.object', {
#             'object': obj
#         })