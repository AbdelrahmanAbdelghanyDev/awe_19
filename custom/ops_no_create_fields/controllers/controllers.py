# -*- coding: utf-8 -*-
# from odoo import http


# class OpsNoCreateFields(http.Controller):
#     @http.route('/ops_no_create_fields/ops_no_create_fields/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ops_no_create_fields/ops_no_create_fields/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ops_no_create_fields.listing', {
#             'root': '/ops_no_create_fields/ops_no_create_fields',
#             'objects': http.request.env['ops_no_create_fields.ops_no_create_fields'].search([]),
#         })

#     @http.route('/ops_no_create_fields/ops_no_create_fields/objects/<model("ops_no_create_fields.ops_no_create_fields"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ops_no_create_fields.object', {
#             'object': obj
#         })
