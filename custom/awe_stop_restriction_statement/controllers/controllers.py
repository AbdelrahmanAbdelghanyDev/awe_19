# -*- coding: utf-8 -*-
# from odoo import http


# class AweStopRestrictionStatement(http.Controller):
#     @http.route('/awe_stop_restriction_statement/awe_stop_restriction_statement', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/awe_stop_restriction_statement/awe_stop_restriction_statement/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('awe_stop_restriction_statement.listing', {
#             'root': '/awe_stop_restriction_statement/awe_stop_restriction_statement',
#             'objects': http.request.env['awe_stop_restriction_statement.awe_stop_restriction_statement'].search([]),
#         })

#     @http.route('/awe_stop_restriction_statement/awe_stop_restriction_statement/objects/<model("awe_stop_restriction_statement.awe_stop_restriction_statement"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('awe_stop_restriction_statement.object', {
#             'object': obj
#         })
