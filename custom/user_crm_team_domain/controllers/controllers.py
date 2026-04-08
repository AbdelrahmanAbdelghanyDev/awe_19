# -*- coding: utf-8 -*-
from odoo import http

# class UserCrmTeamDomain(http.Controller):
#     @http.route('/user_crm_team_domain/user_crm_team_domain/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/user_crm_team_domain/user_crm_team_domain/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('user_crm_team_domain.listing', {
#             'root': '/user_crm_team_domain/user_crm_team_domain',
#             'objects': http.request.env['user_crm_team_domain.user_crm_team_domain'].search([]),
#         })

#     @http.route('/user_crm_team_domain/user_crm_team_domain/objects/<model("user_crm_team_domain.user_crm_team_domain"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('user_crm_team_domain.object', {
#             'object': obj
#         })