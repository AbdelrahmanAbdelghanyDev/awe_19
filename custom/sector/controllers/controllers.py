# -*- coding: utf-8 -*-
from odoo import http

# class Sector(http.Controller):
#     @http.route('/sector/sector/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sector/sector/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sector.listing', {
#             'root': '/sector/sector',
#             'objects': http.request.env['sector.sector'].search([]),
#         })

#     @http.route('/sector/sector/objects/<model("sector.sector"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sector.object', {
#             'object': obj
#         })