# -*- coding: utf-8 -*-
from odoo import http

# class EntryAge(http.Controller):
#     @http.route('/entry_age/entry_age/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/entry_age/entry_age/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('entry_age.listing', {
#             'root': '/entry_age/entry_age',
#             'objects': http.request.env['entry_age.entry_age'].search([]),
#         })

#     @http.route('/entry_age/entry_age/objects/<model("entry_age.entry_age"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('entry_age.object', {
#             'object': obj
#         })