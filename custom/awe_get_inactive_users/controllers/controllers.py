# -*- coding: utf-8 -*-
from odoo import http

# class AweGetInactiveUsers(http.Controller):
#     @http.route('/awe_get_inactive_users/awe_get_inactive_users/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/awe_get_inactive_users/awe_get_inactive_users/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('awe_get_inactive_users.listing', {
#             'root': '/awe_get_inactive_users/awe_get_inactive_users',
#             'objects': http.request.env['awe_get_inactive_users.awe_get_inactive_users'].search([]),
#         })

#     @http.route('/awe_get_inactive_users/awe_get_inactive_users/objects/<model("awe_get_inactive_users.awe_get_inactive_users"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('awe_get_inactive_users.object', {
#             'object': obj
#         })