# -*- coding: utf-8 -*-
from odoo import http

# class AweCustmizeDate(http.Controller):
#     @http.route('/awe_custmize_date/awe_custmize_date/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/awe_custmize_date/awe_custmize_date/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('awe_custmize_date.listing', {
#             'root': '/awe_custmize_date/awe_custmize_date',
#             'objects': http.request.env['awe_custmize_date.awe_custmize_date'].search([]),
#         })

#     @http.route('/awe_custmize_date/awe_custmize_date/objects/<model("awe_custmize_date.awe_custmize_date"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('awe_custmize_date.object', {
#             'object': obj
#         })