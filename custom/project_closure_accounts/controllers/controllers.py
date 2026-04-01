# -*- coding: utf-8 -*-
from odoo import http

# class ProjectClosureAccounts(http.Controller):
#     @http.route('/project_closure_accounts/project_closure_accounts/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_closure_accounts/project_closure_accounts/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_closure_accounts.listing', {
#             'root': '/project_closure_accounts/project_closure_accounts',
#             'objects': http.request.env['project_closure_accounts.project_closure_accounts'].search([]),
#         })

#     @http.route('/project_closure_accounts/project_closure_accounts/objects/<model("project_closure_accounts.project_closure_accounts"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_closure_accounts.object', {
#             'object': obj
#         })