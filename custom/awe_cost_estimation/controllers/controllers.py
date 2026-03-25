# -*- coding: utf-8 -*-
from odoo import http

# class AweCostEstimation(http.Controller):
#     @http.route('/awe_cost_estimation/awe_cost_estimation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/awe_cost_estimation/awe_cost_estimation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('awe_cost_estimation.listing', {
#             'root': '/awe_cost_estimation/awe_cost_estimation',
#             'objects': http.request.env['awe_cost_estimation.awe_cost_estimation'].search([]),
#         })

#     @http.route('/awe_cost_estimation/awe_cost_estimation/objects/<model("awe_cost_estimation.awe_cost_estimation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('awe_cost_estimation.object', {
#             'object': obj
#         })