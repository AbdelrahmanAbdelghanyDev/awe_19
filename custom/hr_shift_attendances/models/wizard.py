# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime, date, timedelta
# from dateutil.relativedelta import relativedelta


class GenerateDaysWizard(models.TransientModel):
    _name = 'wizard.generate.days'

    employees_ids = fields.Many2many('hr.employee', string='Employees')
    start_date = fields.Date(string='From')
    end_date = fields.Date(string='To')
    check_weekends = fields.Boolean('Weekends')
    check_vacations = fields.Boolean('Vacations')
    check_pub_holidays = fields.Boolean('Public Holidays')
    check_absence = fields.Boolean('Absence')



    def action_generate_days(self):
        attendances = self.env['hr.attendance']
        leaves = self.env['hr.holidays']
        pub_holidays = self.env['hr.holidays.public.line']
        calendar_attendances= self.env['resource.calendar.attendance']
        days_between = (datetime.strptime(self.end_date, '%Y-%m-%d') - datetime.strptime(self.start_date, '%Y-%m-%d')).days
        for n in range(days_between+1):
            single_date= (datetime.strptime(self.start_date, '%Y-%m-%d') + timedelta(days=n))
            for emp in self.employees_ids:
                attendance_found_or_created = False
                attendance_found = attendances.search([('employee_id', '=', emp.id), ('custom_date', '=', single_date.date())])
                if not attendance_found:
                    if self.check_pub_holidays and not attendance_found_or_created:
                        pub_holiday_found = pub_holidays.search([('date','=', single_date.date())])
                        if pub_holiday_found:
                            id = attendances.create({
                                'employee_id': emp.id,
                                'check_in': single_date,
                                'check_out': single_date,
                                'remarks': 'Holiday',
                                'display_remarks': pub_holiday_found.name,
                            })
                            attendance_found_or_created=True
                            continue
                    if self.check_vacations and not attendance_found_or_created:
                        leaves_this_emp = leaves.search([('employee_id', '=', emp.id)])
                        for leave in leaves_this_emp:
                            if leave.date_from and leave.date_to:
                                leave_from_date = datetime.strptime(leave.date_from, '%Y-%m-%d %H:%M:%S')
                                leave_to_date = datetime.strptime(leave.date_to, '%Y-%m-%d %H:%M:%S')
                                if (leave_from_date.strftime("%Y-%m-%d") <= single_date.strftime("%Y-%m-%d")) and (leave_to_date.strftime("%Y-%m-%d") >= single_date.strftime("%Y-%m-%d")):
                                    id = attendances.create({
                                        'employee_id': emp.id,
                                        'check_in': single_date,
                                        'check_out': single_date,
                                        'remarks': 'Leave',
                                        'display_remarks':leave.holiday_status_id.name,
                                    })
                                    attendance_found_or_created = True
                                    break
                    if not attendance_found_or_created:
                        weekdays={'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
                        day_name = single_date.date().strftime("%A")
                        workday = calendar_attendances.search([('calendar_id', '=', emp.resource_calendar_id.id),
                                                               ('dayofweek', '=', weekdays[day_name])])
                        if self.check_weekends and not workday:
                            id = attendances.create({
                                'employee_id': emp.id,
                                'check_in': single_date,
                                'check_out': single_date,
                                'remarks': 'Day off',
                                'display_remarks': 'Day off',
                            })
                        elif workday:
                            if self.check_absence:
                                id = attendances.create({
                                    'employee_id': emp.id,
                                    'check_in': single_date,
                                    'check_out': single_date,
                                    'remarks': 'Absent',
                                    'display_remarks': 'Absent',
                                })
