# -*- coding: utf-8 -*-
from odoo import http

# class WorkingScheduleShifts(http.Controller):
#     @http.route('/working_schedule_shifts/working_schedule_shifts/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/working_schedule_shifts/working_schedule_shifts/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('working_schedule_shifts.listing', {
#             'root': '/working_schedule_shifts/working_schedule_shifts',
#             'objects': http.request.env['working_schedule_shifts.working_schedule_shifts'].search([]),
#         })

#     @http.route('/working_schedule_shifts/working_schedule_shifts/objects/<model("working_schedule_shifts.working_schedule_shifts"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('working_schedule_shifts.object', {
#             'object': obj
#         })