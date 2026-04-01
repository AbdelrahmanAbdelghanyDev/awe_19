# -*- coding: utf-8 -*-
# from odoo import http


# class AweProjectMilestonePercentage(http.Controller):
#     @http.route('/awe_project_milestone_percentage/awe_project_milestone_percentage', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/awe_project_milestone_percentage/awe_project_milestone_percentage/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('awe_project_milestone_percentage.listing', {
#             'root': '/awe_project_milestone_percentage/awe_project_milestone_percentage',
#             'objects': http.request.env['awe_project_milestone_percentage.awe_project_milestone_percentage'].search([]),
#         })

#     @http.route('/awe_project_milestone_percentage/awe_project_milestone_percentage/objects/<model("awe_project_milestone_percentage.awe_project_milestone_percentage"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('awe_project_milestone_percentage.object', {
#             'object': obj
#         })
