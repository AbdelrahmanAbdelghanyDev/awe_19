# -*- coding: utf-8 -*-
from odoo import http

# class AccountChatter(http.Controller):
#     @http.route('/account_chatter/account_chatter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_chatter/account_chatter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_chatter.listing', {
#             'root': '/account_chatter/account_chatter',
#             'objects': http.request.env['account_chatter.account_chatter'].search([]),
#         })

#     @http.route('/account_chatter/account_chatter/objects/<model("account_chatter.account_chatter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_chatter.object', {
#             'object': obj
#         })