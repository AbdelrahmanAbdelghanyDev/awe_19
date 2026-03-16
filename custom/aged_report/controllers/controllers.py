# -*- coding: utf-8 -*-
from odoo import http

# class AgedReport(http.Controller):
#     @http.route('/aged_report/aged_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aged_report/aged_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aged_report.listing', {
#             'root': '/aged_report/aged_report',
#             'objects': http.request.env['aged_report.aged_report'].search([]),
#         })

#     @http.route('/aged_report/aged_report/objects/<model("aged_report.aged_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aged_report.object', {
#             'object': obj
#         })