# -*- coding: utf-8 -*-
from odoo import http

# class Requestioner(http.Controller):
#     @http.route('/requestioner/requestioner/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/requestioner/requestioner/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('requestioner.listing', {
#             'root': '/requestioner/requestioner',
#             'objects': http.request.env['requestioner.requestioner'].search([]),
#         })

#     @http.route('/requestioner/requestioner/objects/<model("requestioner.requestioner"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('requestioner.object', {
#             'object': obj
#         })