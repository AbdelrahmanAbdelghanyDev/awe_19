# -*- coding: utf-8 -*-
from odoo import http

# class AweOfficialName(http.Controller):
#     @http.route('/awe_official_name/awe_official_name/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/awe_official_name/awe_official_name/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('awe_official_name.listing', {
#             'root': '/awe_official_name/awe_official_name',
#             'objects': http.request.env['awe_official_name.awe_official_name'].search([]),
#         })

#     @http.route('/awe_official_name/awe_official_name/objects/<model("awe_official_name.awe_official_name"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('awe_official_name.object', {
#             'object': obj
#         })