# -*- coding: utf-8 -*-
from odoo import http

# class NewAweEdits(http.Controller):
#     @http.route('/new_awe_edits/new_awe_edits/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/new_awe_edits/new_awe_edits/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('new_awe_edits.listing', {
#             'root': '/new_awe_edits/new_awe_edits',
#             'objects': http.request.env['new_awe_edits.new_awe_edits'].search([]),
#         })

#     @http.route('/new_awe_edits/new_awe_edits/objects/<model("new_awe_edits.new_awe_edits"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('new_awe_edits.object', {
#             'object': obj
#         })