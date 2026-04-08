# -*- coding: utf-8 -*-
from odoo import http

# class MulticurrencyRevaluation(http.Controller):
#     @http.route('/multicurrency_revaluation/multicurrency_revaluation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/multicurrency_revaluation/multicurrency_revaluation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('multicurrency_revaluation.listing', {
#             'root': '/multicurrency_revaluation/multicurrency_revaluation',
#             'objects': http.request.env['multicurrency_revaluation.multicurrency_revaluation'].search([]),
#         })

#     @http.route('/multicurrency_revaluation/multicurrency_revaluation/objects/<model("multicurrency_revaluation.multicurrency_revaluation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('multicurrency_revaluation.object', {
#             'object': obj
#         })