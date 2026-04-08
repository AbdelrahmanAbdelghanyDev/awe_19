from odoo.http import Controller, request, route
from datetime import datetime, timedelta

class LeavePortal(Controller):
    @route(['/my/attendance'], type='http', auth="user", website=True)
    def attendance(self, **kw):
        vals = {}
        employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', request.uid)])
        if employee_id:
            attendance_id = request.env['hr.attendance'].sudo().search([('employee_id', '=', employee_id.id)],limit=1,order='id desc')
            if (not attendance_id) or (attendance_id.check_in and attendance_id.check_out):
                attendance_status = 'check_in'
            else:
                attendance_status = 'check_out'
        else:
            attendance_status = 'not_available'
        print(attendance_status)
        vals = {'attendance_status':attendance_status}
        return request.render("portal_attendance.attendance",vals)

    @route(['/check_in'], type='http', auth="user", website=True)
    def check_in(self, **kw):
        employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', request.uid)])
        if employee_id:
            request.env['hr.attendance'].sudo().create({'employee_id':employee_id.id,
                                                        'check_in':datetime.now()+ timedelta(hours=2)})
        return request.render("portal_attendance.checked_in")

    @route(['/check_out'], type='http', auth="user", website=True)
    def check_out(self, **kw):
        employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', request.uid)])
        if employee_id:
            request.env['hr.attendance'].sudo().search([('employee_id', '=', employee_id.id)], limit=1,
                                                       order='id desc').write({'check_out':datetime.now()+ timedelta(hours=2)})

        return request.render("portal_attendance.checked_out")