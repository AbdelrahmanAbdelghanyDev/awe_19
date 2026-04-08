# -*- coding: utf-8 -*-
# from odoo import http


# class TaskTotalCost(http.Controller):
#     @http.route('/task_total_cost/task_total_cost', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/task_total_cost/task_total_cost/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('task_total_cost.listing', {
#             'root': '/task_total_cost/task_total_cost',
#             'objects': http.request.env['task_total_cost.task_total_cost'].search([]),
#         })

#     @http.route('/task_total_cost/task_total_cost/objects/<model("task_total_cost.task_total_cost"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('task_total_cost.object', {
#             'object': obj
#         })
