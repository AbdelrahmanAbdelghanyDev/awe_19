# -*- coding: utf-8 -*-
from odoo import http

# class /odoo13e/custom/addons/currencyChange/(http.Controller):
#     @http.route('//odoo13e/custom/addons/currency_change///odoo13e/custom/addons/currency_change//', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//odoo13e/custom/addons/currency_change///odoo13e/custom/addons/currency_change//objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/odoo13e/custom/addons/currency_change/.listing', {
#             'root': '//odoo13e/custom/addons/currency_change///odoo13e/custom/addons/currency_change/',
#             'objects': http.request.env['/odoo13e/custom/addons/currency_change/./odoo13e/custom/addons/currency_change/'].search([]),
#         })

#     @http.route('//odoo13e/custom/addons/currency_change///odoo13e/custom/addons/currency_change//objects/<model("/odoo13e/custom/addons/currency_change/./odoo13e/custom/addons/currency_change/"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/odoo13e/custom/addons/currency_change/.object', {
#             'object': obj
#         })