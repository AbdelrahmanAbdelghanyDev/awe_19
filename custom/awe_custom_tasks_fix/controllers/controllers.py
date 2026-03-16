# -*- coding: utf-8 -*-
# from odoo import http


# class AweCustomTasksFix(http.Controller):
#     @http.route('/awe_custom_tasks_fix/awe_custom_tasks_fix', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/awe_custom_tasks_fix/awe_custom_tasks_fix/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('awe_custom_tasks_fix.listing', {
#             'root': '/awe_custom_tasks_fix/awe_custom_tasks_fix',
#             'objects': http.request.env['awe_custom_tasks_fix.awe_custom_tasks_fix'].search([]),
#         })

#     @http.route('/awe_custom_tasks_fix/awe_custom_tasks_fix/objects/<model("awe_custom_tasks_fix.awe_custom_tasks_fix"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('awe_custom_tasks_fix.object', {
#             'object': obj
#         })
