# -*- coding: utf-8 -*-
# from odoo import http


# class AweCurrencyNum2words(http.Controller):
#     @http.route('/awe_currency_num2words/awe_currency_num2words', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/awe_currency_num2words/awe_currency_num2words/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('awe_currency_num2words.listing', {
#             'root': '/awe_currency_num2words/awe_currency_num2words',
#             'objects': http.request.env['awe_currency_num2words.awe_currency_num2words'].search([]),
#         })

#     @http.route('/awe_currency_num2words/awe_currency_num2words/objects/<model("awe_currency_num2words.awe_currency_num2words"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('awe_currency_num2words.object', {
#             'object': obj
#         })
