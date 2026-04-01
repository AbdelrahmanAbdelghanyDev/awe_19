# -*- coding: utf-8 -*-
from odoo import http

# class HrShiftAttendances(http.Controller):
#     @http.route('/hr_shift_attendances/hr_shift_attendances/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_shift_attendances/hr_shift_attendances/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_shift_attendances.listing', {
#             'root': '/hr_shift_attendances/hr_shift_attendances',
#             'objects': http.request.env['hr_shift_attendances.hr_shift_attendances'].search([]),
#         })

#     @http.route('/hr_shift_attendances/hr_shift_attendances/objects/<model("hr_shift_attendances.hr_shift_attendances"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_shift_attendances.object', {
#             'object': obj
#         })