# -*- coding: utf-8 -*-
from odoo import http

# class PaymentMode(http.Controller):
#     @http.route('/payment_mode/payment_mode/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payment_mode/payment_mode/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('payment_mode.listing', {
#             'root': '/payment_mode/payment_mode',
#             'objects': http.request.env['payment_mode.payment_mode'].search([]),
#         })

#     @http.route('/payment_mode/payment_mode/objects/<model("payment_mode.payment_mode"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payment_mode.object', {
#             'object': obj
#         })