# -*- coding: utf-8 -*-
from odoo import http

# class ChangeCurrencyRateFormat(http.Controller):
#     @http.route('/change_currency_rate_format/change_currency_rate_format/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/change_currency_rate_format/change_currency_rate_format/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('change_currency_rate_format.listing', {
#             'root': '/change_currency_rate_format/change_currency_rate_format',
#             'objects': http.request.env['change_currency_rate_format.change_currency_rate_format'].search([]),
#         })

#     @http.route('/change_currency_rate_format/change_currency_rate_format/objects/<model("change_currency_rate_format.change_currency_rate_format"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('change_currency_rate_format.object', {
#             'object': obj
#         })