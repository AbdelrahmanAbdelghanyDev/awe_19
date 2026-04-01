# -*- coding: utf-8 -*-
from odoo import http

# class CustomFleet(http.Controller):
#     @http.route('/custom_fleet/custom_fleet/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_fleet/custom_fleet/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_fleet.listing', {
#             'root': '/custom_fleet/custom_fleet',
#             'objects': http.request.env['custom_fleet.custom_fleet'].search([]),
#         })

#     @http.route('/custom_fleet/custom_fleet/objects/<model("custom_fleet.custom_fleet"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_fleet.object', {
#             'object': obj
#         })