# -*- coding: utf-8 -*-
# from odoo import http


# class TimeCostEstimation(http.Controller):
#     @http.route('/time_cost_estimation/time_cost_estimation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/time_cost_estimation/time_cost_estimation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('time_cost_estimation.listing', {
#             'root': '/time_cost_estimation/time_cost_estimation',
#             'objects': http.request.env['time_cost_estimation.time_cost_estimation'].search([]),
#         })

#     @http.route('/time_cost_estimation/time_cost_estimation/objects/<model("time_cost_estimation.time_cost_estimation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('time_cost_estimation.object', {
#             'object': obj
#         })
