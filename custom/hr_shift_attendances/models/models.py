# -*- coding: utf-8 -*-
import datetime
import math
from datetime import datetime, timedelta, date, time
import calendar

from odoo import api, fields, models, tools, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

import logging

_logger = logging.getLogger(__name__)


class CustomEmployee(models.Model):
    _inherit = 'hr.employee'

    working_time = fields.Selection([('standard', 'Standard'), ('shifts', 'Shifts')], 'Working Time')


class NotifyMessage(models.Model):
    _inherit = 'mail.message'

    def notify_user_attend(self, employee, date, custom_in, custom_out):
        try:
            user = self.env["hr.employee"].browse(employee)
        except Exception as e:
            pass

        template_obj = self.env['mail.template'].sudo().search([('name', '=', 'Attendance Notification')], limit=1)
        body = template_obj.body_html

        date = str(date).split()[0]
        send_mail = self.env['ir.mail_server'].search([])

        body = "Dear " + user.lastname + " " + user.firstname + ', <br>' + "We would notify you " + "in " + date + " " + "your check in is " + custom_in + '<br>' + "and your check out is " + " " + custom_out
        mail_values = {
            'subject': "Attendance notification",
            'body_html': body,
            'email_to': user.work_email,
            'email_from': send_mail.smtp_user  # template_obj.email_from,
        }
        self.env['mail.mail'].create(mail_values).send()


class HrAttendanceCustom(models.Model):
    _inherit = 'hr.attendance'

    custom_date = fields.Date(compute='_compute_custom_date', store=True)
    custom_in = fields.Char(compute='_compute_custom_date', store=True)  # Time Clock format
    custom_out = fields.Char(compute='_compute_custom_out', store=True)  # Time Clock format

    custom_normal_hours = fields.Float(compute='_compute_working_hours_per_day', store=True)
    custom_over_time = fields.Float(compute='_compute_working_hours_per_day', store=True)
    custom_over_time_1 = fields.Float(compute='_compute_working_hours_per_day', store=True)
    custom_over_time_2 = fields.Float(compute='_compute_working_hours_per_day', store=True)
    custom_over_time_3 = fields.Float(compute='_compute_working_hours_per_day', store=True)

    working_hours_per_day = fields.Float(compute='_compute_working_hours_per_day', store=True)

    is_late = fields.Boolean(compute='_compute_is_late', store=True)
    is_early = fields.Boolean(compute='_compute_is_early', store=True)

    is_late_time = fields.Float(compute='_compute_is_late', string="Late IN", store=True)
    is_early_time = fields.Float(compute='_compute_is_early', string="Early OUT", store=True)

    remarks = fields.Char(string='Remarks')
    display_remarks = fields.Char(string='Remarks')

    resource_calendar_id = fields.Many2one('resource.calendar')

    @api.model
    def create(self, vals):
        record = super(HrAttendanceCustom, self).create(vals)

        is_shift_emp = (record.employee_id.working_time == 'shifts')
        if is_shift_emp and record.remarks in ['Absent', 'Day off', 'Shift', '', False]:
            date = datetime.strptime(record.check_in, '%Y-%m-%d %H:%M:%S')
            shifts = self.env['calendar.month.day'].search([('day', '=', date)])
            for shift in shifts:
                is_in_shift = False
                for employee in shift.employees_ids:
                    if employee.id == record.employee_id.id:
                        is_in_shift = True
                        record.resource_calendar_id = shift.calendar_month_id.resource_calendar_id.id
                        record.remarks = 'Shift'
                        record.display_remarks = 'Shift'
                        record._compute_is_early()
                        record._compute_is_late()
                        record._compute_working_hours_per_day()
                        if record.custom_normal_hours == 0 and record.working_hours_per_day > 0:
                            record.remarks = 'Overtime'
                            record.display_remarks = 'Overtime'
                        elif record.custom_normal_hours == 0:
                            record.remarks = 'Day off'
                            record.display_remarks = 'Day off'
                        elif record.custom_normal_hours != 0 and record.working_hours_per_day == 0:
                            record.remarks = 'Absent'
                            record.display_remarks = 'Absent'
                        break
                if not is_in_shift and record.working_hours_per_day != 0:
                    record.remarks = 'Overtime'
                    record.display_remarks = 'Overtime'
            if not shifts and record.working_hours_per_day != 0:
                record.remarks = 'Overtime'
                record.display_remarks = 'Overtime'

        if not record.resource_calendar_id:
            record.resource_calendar_id = record.employee_id.resource_calendar_id.id
        # print(record.resource_calendar_id.name)

        return record


    @api.depends('check_in')
    def _compute_custom_date(self):
        for rec in self:
            if rec.check_in:
                # convert + timezone
                dt = fields.Datetime.context_timestamp(
                    rec,
                    fields.Datetime.from_string(rec.check_in)
                )
                # date
                rec.custom_date = dt.date()

                # time (HH:MM)
                rec.custom_in = dt.strftime('%H:%M')
            else:
                rec.custom_date = False
                rec.custom_in = False

    @api.depends('check_out')
    def _compute_custom_out(self):
        try:
            tmp_date = fields.Datetime.to_string(
                fields.Datetime.context_timestamp(self, fields.Datetime.from_string(self.check_out)))
            self.custom_out = str(tmp_date).split()[1][0:5]
            # try:
            #     if self.custom_in == self.custom_out:
            #         obj = self.env['mail.message'].search([])[0]
            #         obj.notify_user_attend(self.employee_id.id,tmp_date,self.custom_in, self.custom_out)
            # except Exception as e:
            #     pass
            if self.custom_in == self.custom_out:
                obj = self.env['mail.message'].search([])[0]
                obj.notify_user_attend(self.employee_id.id, tmp_date, self.custom_in, self.custom_out)
        except Exception as e:
            pass

    #
    def float_time_convert(self, float_val):
        factor = float_val < 0 and -1 or 1
        val = abs(float_val)
        return (factor * int(math.floor(val)), int(round((val % 1) * 60)))

    # ...


    def write(self, vals):
        if 'remarks' in vals:
            if self.remarks != vals['remarks']:
                # vals['remarks'] = self.remarks
                vals['display_remarks'] = vals['remarks']  # self.display_remarks
        elif 'display_remarks' in vals:
            # if vals['remarks'] =='Overtime' and 'working_hours_per_day' not in vals:
            if self.display_remarks != vals['display_remarks']:
                vals['remarks'] = vals['display_remarks']  # self.remarks
                # vals['display_remarks'] = self.display_remarks
        return super(HrAttendanceCustom, self).write(vals)

        # print('writeeeeeee',self.remarks)


    @api.depends('check_in', 'check_out')
    def _compute_working_hours_per_day(self):
        return
        # print('remarksssssssss', self.remarks)
        # if self.remarks:
        #     return
        for rec in self:
            if (rec.check_out):
                tmp_time = (datetime.strptime(rec.check_out, DEFAULT_SERVER_DATETIME_FORMAT) - datetime.strptime(
                    rec.check_in, DEFAULT_SERVER_DATETIME_FORMAT)).total_seconds() / 3600.0
                rec.working_hours_per_day = (timedelta(hours=float(tmp_time)).total_seconds()) / 3600.0

                # contract = rec.env['hr.contract'].search(
                #     [('employee_id', '=', rec.employee_id.id), ('state', '=', 'open')])
                working_hours = 0

                # if (contract):
                #     contract = contract[0]
                # days = contract.working_hours.attendance_ids
                if rec.resource_calendar_id:
                    days = rec.resource_calendar_id.attendance_ids
                    try:
                        date_from_str = fields.Datetime.context_timestamp(rec,
                                                                          fields.Datetime.from_string(rec.check_in))
                    except:
                        return
                    checkin_day = date_from_str.strftime("%A")
                    name_of_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    schedule_in = 0.0
                    schedule_out = 0.0
                    for day in days:
                        if (name_of_days[int(day.dayofweek)] == checkin_day):
                            late = day.late_time
                            # hour, minute = rec.float_time_convert(day.hour_from)
                            schedule_in = day.hour_from
                            schedule_out = day.hour_to
                            working_hours = day.working_hours
                            break
                    if rec.custom_out:
                        attendance_in = float(rec.custom_in.split(':')[0]) + float(rec.custom_in.split(':')[1]) / 60
                        attendance_out = float(rec.custom_out.split(':')[0]) + float(rec.custom_out.split(':')[1]) / 60
                        if attendance_in > schedule_out:
                            if rec.remarks in ['Absent', 'Day off', 'Leave', 'Shift']:
                                return
                            # rec.remarks = 'Overtime'
                            # rec.display_remarks = 'Overtime'
                            rec.write({'remarks': 'Overtime'})
                            rec.write({'display_remarks': 'Overtime'})
                            rec.custom_normal_hours = 0
                        elif attendance_in >= schedule_in:  # (float(rec.custom_in.split(':')[0])+float(rec.custom_in.split(':')[1])/60) > temp_in:
                            if attendance_out >= schedule_out:
                                rec.custom_normal_hours = schedule_out - attendance_in
                            else:
                                rec.custom_normal_hours = attendance_out - attendance_in
                        else:
                            if attendance_out >= schedule_out:
                                rec.custom_normal_hours = schedule_out - schedule_in
                            else:
                                rec.custom_normal_hours = attendance_out - schedule_in

                # rec.custom_normal_hours =
                if ((float(
                        tmp_time) > working_hours and working_hours != 0)):  # or (working_hours < rec.custom_normal_hours and working_hours!=0)):

                    # rec.custom_normal_hours = working_hours
                    rec.custom_over_time = (timedelta(hours=float(tmp_time - working_hours)).total_seconds()) / 3600.0
                    rec.write({'remarks': 'Overtime'})
                    rec.write({'display_remarks': 'Overtime'})
                    # rec.remarks = 'Overtime'
                    # rec.display_remarks = 'Overtime'
                else:
                    # rec.custom_normal_hours = tmp_time
                    rec.custom_over_time = 0

            # print('custom normal hours', self.custom_normal_hours)

            def calcualte_total_time(time_str):  # time_str is a list of times.
                minutes = 0
                for i in time_str:
                    try:
                        d = i.split(',')[0].split()[0]
                        h, m = i.split(',')[1].split(':')
                        h = "".join(h.split())
                        minutes += (int(d) * 24 * 3600 + int(h) * 3600 + int(m) * 60) / 60.0
                    except:
                        try:
                            h, m, s = i.split(':')
                            minutes += (int(h) * 3600 + int(m) * 60 + int(s)) / 60.0
                        except:
                            h, m = i.split(':')
                            minutes += (int(h) * 3600 + int(m) * 60) / 60.0

                return minutes / 60

            overtime_hours = self.custom_over_time
            overtime_starting_period = datetime.strptime(self.check_out, DEFAULT_SERVER_DATETIME_FORMAT) - timedelta(
                hours=overtime_hours)
            overtime_ending_period = datetime.strptime(self.check_out, DEFAULT_SERVER_DATETIME_FORMAT)

            # overtime_ending_period = overtime_ending_period + timedelta(hours=2) ## Manual timezone

            # overtime_ending_period must be in current timezone so that to be consistent with the overtime
            # hardcoded times implemented below (4:00 & 21:00)
            overtime_ending_period = fields.Datetime.context_timestamp(self, fields.Datetime.from_string(
                str(overtime_ending_period)))
            overtime_ending_period = datetime.strptime(str(overtime_ending_period)[:-6], '%Y-%m-%d %H:%M:%S')

            overtime_hours_period_1 = 0
            overtime_hours_period_2 = 0

            skip_flag = False

            while (overtime_hours > 0):
                tmp = datetime.strptime(str(overtime_ending_period).split()[0],
                                        '%Y-%m-%d').date()  ## Danger time format
                if not skip_flag:  ## values for 4,00 & 21,00 are hardcoded, need to be fixed.
                    period_1_start = datetime.combine(tmp, time(4, 00))
                    period_1_end = datetime.combine(tmp, time(21, 00))
                    period_2_start = datetime.combine(tmp, time(21, 00))
                    period_2_end = datetime.combine(tmp + timedelta(days=1), time(4, 00))
                elif skip_flag:
                    period_1_start = datetime.combine(tmp - timedelta(days=1), time(4, 00))
                    period_1_end = datetime.combine(tmp - timedelta(days=1), time(21, 00))
                    period_2_start = datetime.combine(tmp - timedelta(days=1), time(21, 00))
                    period_2_end = datetime.combine(tmp, time(4, 00))

                if overtime_ending_period > period_1_start and overtime_ending_period <= period_1_end:
                    skip_flag = False
                    if overtime_hours > calcualte_total_time([str(overtime_ending_period - period_1_start)]):
                        overtime_hours -= calcualte_total_time([str(overtime_ending_period - period_1_start)])
                        overtime_hours_period_1 += calcualte_total_time([str(overtime_ending_period - period_1_start)])
                        overtime_ending_period -= timedelta(
                            hours=calcualte_total_time([str(overtime_ending_period - period_1_start)]))

                    elif overtime_hours <= calcualte_total_time([str(overtime_ending_period - period_1_start)]):
                        overtime_hours_period_1 += overtime_hours
                        overtime_hours -= overtime_hours
                        overtime_ending_period = overtime_ending_period - timedelta(hours=overtime_hours)

                elif overtime_ending_period > period_2_start and overtime_ending_period <= period_2_end:
                    skip_flag = False
                    if overtime_hours > calcualte_total_time([str(overtime_ending_period - period_2_start)]):
                        overtime_hours -= calcualte_total_time([str(overtime_ending_period - period_2_start)])
                        overtime_hours_period_2 += calcualte_total_time([str(overtime_ending_period - period_2_start)])
                        overtime_ending_period -= timedelta(
                            hours=calcualte_total_time([str(overtime_ending_period - period_2_start)]))

                    elif overtime_hours <= calcualte_total_time([str(overtime_ending_period - period_2_start)]):
                        overtime_hours_period_2 += overtime_hours
                        overtime_hours -= overtime_hours
                        overtime_ending_period = overtime_ending_period - timedelta(hours=overtime_hours)

                elif overtime_ending_period <= period_1_start:
                    skip_flag = True


                elif calcualte_total_time([str(overtime_ending_period - period_1_start)]) == 0:
                    ## Inspect this condition, may be useless !!.
                    overtime_hours_period_2 += 1
                    overtime_hours -= 1
                    overtime_ending_period = overtime_ending_period - timedelta(hours=1)
                    skip_flag = True

            if working_hours != 0:
                self.custom_over_time_1 = (timedelta(hours=float(overtime_hours_period_1)).total_seconds()) / 3600.0
                self.custom_over_time_2 = (timedelta(hours=float(overtime_hours_period_2)).total_seconds()) / 3600.0
                self.custom_over_time_3 = 0
            elif working_hours == 0:
                self.custom_over_time_1 = 0
                self.custom_over_time_2 = 0
                self.custom_over_time_3 = self.custom_over_time


    @api.depends('check_in')
    def _compute_is_late(self):
        # contract = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id), ('state', '=', 'open')])
        # if (contract):
        #     contract = contract[0]
        #     days = contract.working_hours.attendance_ids
        if self.resource_calendar_id:
            days = self.resource_calendar_id.attendance_ids
            try:
                date_from_str = fields.Datetime.context_timestamp(self, fields.Datetime.from_string(self.check_in))
            except:
                return
            checkin_day = date_from_str.strftime("%A")
            late = -1
            origin_time = -1
            name_of_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for day in days:
                if name_of_days[int(day.dayofweek)] == checkin_day:
                    late = day.late_time
                    origin_time = day.hour_from
                    break
            if origin_time == -1:
                self.is_late = False
                return
            temp_date = date_from_str
            temp_date = temp_date.replace(hour=int(origin_time), minute=0, second=0)

            if date_from_str > temp_date:
                diff_time = (date_from_str - temp_date).seconds
                if diff_time <= late * 60:
                    self.is_late = False
                else:
                    self.is_late = True
                    self.is_late_time = (timedelta(seconds=float(diff_time)).total_seconds()) / 3600.0
            else:
                self.is_late = False
        else:
            self.is_late = False


    @api.depends('check_out')
    def _compute_is_early(self):
        # contract = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id), ('state', '=', 'open')])
        # if (contract):
        #     contract = contract[0]
        #     days = contract.working_hours.attendance_ids
        if self.resource_calendar_id:
            days = self.resource_calendar_id.attendance_ids
            try:
                date_from_str = fields.Datetime.context_timestamp(self, fields.Datetime.from_string(self.check_out))
                if self.custom_over_time != 0:
                    return
            except:
                return
            checkout_day = date_from_str.strftime("%A")
            early = 0
            origin_time = 0
            name_of_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for day in days:
                if (name_of_days[int(day.dayofweek)] == checkout_day):
                    early = day.early_time
                    origin_time = day.hour_to
                    break

            temp_date = date_from_str
            temp_date = temp_date.replace(hour=int(origin_time), minute=0, second=0)

            if (date_from_str < temp_date):
                diff_time = (temp_date - date_from_str).seconds

                if (diff_time <= early * 60):
                    self.is_early = False
                else:
                    self.is_early = True
                    self.is_early_time = (timedelta(seconds=float(diff_time)).total_seconds()) / 3600.0
            else:
                self.is_early = False
        else:
            self.is_early = False


class ResourceCalendarAttendanceCustom(models.Model):
    _inherit = 'resource.calendar.attendance'

    late_time = fields.Integer("Late Time")
    early_time = fields.Integer("Early Time")
    working_hours = fields.Float("Working hours", compute='_compute_working_hours')


    @api.depends('hour_from', 'hour_to')
    def _compute_working_hours(self):
        for rec in self:
            rec.working_hours = rec.hour_to - rec.hour_from


class PayRollCustom(models.Model):
    _inherit = 'hr.payslip'

    # contract_id = fields.Many2one('hr.contract', string='Contract', required=True,
    #                               help="The contract for which applied this input",
    #                               domain=[('state', '=', 'open')])

    @api.model
    def get_worked_day_lines(self, contract_ids, date_from, date_to):

        res = super(PayRollCustom, self).get_worked_day_lines(contract_ids, date_from, date_to)

        def calcualte_total_time(time_str):
            minutes = 0
            for i in time_str:
                try:
                    d = i.split(',')[0].split()[0]
                    h, m = i.split(',')[1].split(':')
                    h = "".join(h.split())
                    minutes += (int(d) * 24 * 3600 + int(h) * 3600 + int(m) * 60) / 60.0
                except:
                    h, m = i.split(':')
                    minutes += (int(h) * 3600 + int(m) * 60) / 60.0

            return minutes / 60

        class DateDay:
            def __init__(self, date, day, attended=False):
                self.date = date
                self.day = day
                self.attended = attended

        from datetime import date
        _logger.error('get_worked_day_lines date_from ')
        # _logger.error(date_from)
        # _logger.error(date_to)
        date_from = date_from.split(' ')[0]
        date_to = date_to.split(' ')[0]
        _logger.error(date_from)
        _logger.error(date_to)
        # d1 = date(int(date_from.split('-')[0]),
        #           int(date_from.split('-')[1]),
        #           int(date_from.split('-')[2]))
        d1 = fields.Date.from_string(date_from)

        # d2 = date(int(date_to.split('-')[0]),
        #           int(date_to.split('-')[1]),
        #           int(date_to.split('-')[2]))
        d2 = fields.Date.from_string(date_to)

        delta = d2 - d1  # timedelta
        _logger.error(delta)
        days_range = {}
        for i in range(delta.days + 1):
            day = calendar.day_name[
                datetime.strptime(str(d1 + timedelta(days=i)), '%Y-%m-%d').weekday()]  ## Danger time format
            date = str(d1 + timedelta(days=i))
            days_range[date] = DateDay(date, day)

        total_worked_days = 0
        total_overtime_days = 0
        total_overtime_days_1 = 0
        total_overtime_days_2 = 0
        total_overtime_days_3 = 0
        late_early_days = 0

        late_early_hours = []
        total_worked_hours = []
        total_overtime_hours = []
        total_overtime_hours_1 = []
        total_overtime_hours_2 = []
        total_overtime_hours_3 = []

        # contract = self.env['hr.contract'].search([('employee_id','=',self.employee_id.id)])
        # contract = self.contract_id

        if self.contract_id:
            contract = self.contract_id
        # else:
        #     if len(contract_ids) == 1:
        #         contract = self.env['hr.contract'].browse(contract_ids[0].id)
        #     else:
        #         contract = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id),
        #                                                    ('state', '=', 'open')])

        for i in self.env['hr.attendance'].search([('employee_id', '=', contract.employee_id.id),
                                                   ('custom_date', '>=', date_from),
                                                   ('custom_date', '<=', date_to)]):
            # if (contract):
            #     contract = contract[0]
            #     days = contract.working_hours.attendance_ids
            if self.employee_id.resource_calendar_id:
                days = self.employee_id.resource_calendar_id.attendance_ids

                date_from_str = datetime(int(i.custom_date.split('-')[0]), int(i.custom_date.split('-')[1]),
                                         int(i.custom_date.split('-')[2]))  ## Danger when time format changes
                checkin_day = date_from_str.strftime("%A")
                name_of_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                for day in days:
                    if (name_of_days[int(day.dayofweek)] == checkin_day):
                        # calculate total worked days without holidays and overtime days.
                        total_worked_days += 1
                        total_worked_hours.append(i.custom_normal_hours)
                        days_range[str(date_from_str).split()[0]].attended = True

                        # calculates late and early time
                        if i.is_late or i.is_early:
                            if i.is_late:
                                late_early_hours.append(i.is_late_time)
                            if i.is_early:
                                late_early_hours.append(i.is_early_time)

            # calculates overtime.
            if i.custom_over_time != 0:
                total_overtime_hours.append(i.custom_over_time)
            if i.custom_over_time_1 != 0:
                total_overtime_hours_1.append(i.custom_over_time_1)
            if i.custom_over_time_2 != 0:
                total_overtime_hours_2.append(i.custom_over_time_2)
            if i.custom_over_time_3 != 0:
                total_overtime_hours_3.append(i.custom_over_time_3)

        absent_days = 0
        absent_hours = 0
        for i in days_range:
            if days_range[i].attended == True:
                continue
            else:
                # days = contract.working_hours.attendance_ids
                days = self.employee_id.resource_calendar_id.attendance_ids

                date_from_str = datetime(int(i.split('-')[0]), int(i.split('-')[1]),
                                         int(i.split('-')[2]))  ## Danger when time format changes
                checkin_day = date_from_str.strftime("%A")
                name_of_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                for day in days:
                    if (name_of_days[int(day.dayofweek)] == checkin_day):
                        absent_hours = absent_hours + day.working_hours
                        # i.custom_normal_hours = day.working_hours

        # Convert from HH:MM to float format.
        # Values returned in Hours (float)
        total_worked_hours = sum(total_worked_hours)
        total_overtime_hours = sum(total_overtime_hours)
        total_overtime_hours_1 = sum(total_overtime_hours_1)
        total_overtime_hours_2 = sum(total_overtime_hours_2)
        total_overtime_hours_3 = sum(total_overtime_hours_3)
        late_early_hours = sum(late_early_hours)

        try:
            working_day_hours = days[0].working_hours
            total_overtime_days = total_overtime_hours / working_day_hours
            total_overtime_days_1 = total_overtime_hours_1 / working_day_hours
            total_overtime_days_2 = total_overtime_hours_2 / working_day_hours
            total_overtime_days_3 = total_overtime_hours_3 / working_day_hours
            late_early_days = late_early_hours / working_day_hours
            absent_days = absent_hours / working_day_hours

        except:
            # from odoo.osv import osv
            # raise osv.except_osv('Error!',
            #                      'Working Schedule is not specified in the employee\'s contract.')
            pass
            return res
        if len(res) > 0:
            ideal_number_of_days = res[0]['number_of_days']  ## Official days from contract
            ideal_number_of_hours = res[0]['number_of_hours']  ## Official hours from contract

            # res.append({'code':'OVERTIME', 'contract_id':res[0]['contract_id'], 'sequence':10, 'number_of_days':total_overtime_days, 'number_of_hours':total_overtime_hours, 'name':'OverTime.'})

            # recently commented 28-11
            # if contract.overtime:
            #     res.append({'code': 'OVERTIME_1', 'contract_id': res[0]['contract_id'], 'sequence': 10,
            #                 'number_of_days': total_overtime_days_1, 'number_of_hours': total_overtime_hours_1,
            #                 'name': 'OT 4:00,21:00'})
            #     res.append({'code': 'OVERTIME_2', 'contract_id': res[0]['contract_id'], 'sequence': 10,
            #                 'number_of_days': total_overtime_days_2, 'number_of_hours': total_overtime_hours_2,
            #                 'name': 'OT 21:00,4:00'})
            #     res.append({'code': 'OVERTIME_3', 'contract_id': res[0]['contract_id'], 'sequence': 10,
            #                 'number_of_days': total_overtime_days_3, 'number_of_hours': total_overtime_hours_3,
            #                 'name': 'SOT'})
            # else:
            #     res.append({'code': 'OVERTIME_1', 'contract_id': res[0]['contract_id'], 'sequence': 10, 'number_of_days': 0,
            #                 'number_of_hours': 0, 'name': 'OT 4:00,21:00'})
            #     res.append({'code': 'OVERTIME_2', 'contract_id': res[0]['contract_id'], 'sequence': 10, 'number_of_days': 0,
            #                 'number_of_hours': 0, 'name': 'OT 21:00,4:00'})
            #     res.append({'code': 'OVERTIME_3', 'contract_id': res[0]['contract_id'], 'sequence': 10, 'number_of_days': 0,
            #                 'number_of_hours': 0, 'name': 'SOT'})

            res.append({'code': 'LATE', 'contract_id': res[0]['contract_id'], 'sequence': 10,
                        'number_of_days': late_early_days * -1, 'number_of_hours': late_early_hours * -1,
                        'name': 'latness.'})
            res.append(
                {'code': 'ABSENT', 'contract_id': res[0]['contract_id'], 'sequence': 10,
                 'number_of_days': absent_days * -1,
                 'number_of_hours': absent_hours * -1, 'name': 'Absent days.'})

            # Adding the holidays days to the Working hours.
            delta_days = int(delta.days)
            if delta_days + 1 > res[0]['number_of_hours'] / working_day_hours:
                if delta_days + 1 in [28, 29, 30, 31]:
                    delta_days = 29
                res[0]['number_of_days'] = res[0]['number_of_hours'] / working_day_hours
                res[0]['number_of_days'] += (delta_days + 1) - res[0]['number_of_days']
                res[0]['number_of_hours'] = res[0]['number_of_days'] * working_day_hours
            else:
                res[0]['number_of_days'] = res[0]['number_of_hours'] / working_day_hours

        return res

    @api.model
    def get_payslip_lines(self, contract_ids, payslip_id):
        def _sum_salary_rule_category(localdict, category, amount):
            if category.parent_id:
                localdict = _sum_salary_rule_category(localdict, category.parent_id, amount)
            if category.code in localdict['categories'].dict:
                amount += localdict['categories'].dict[category.code]
            localdict['categories'].dict[category.code] = amount
            return localdict

        class BrowsableObject(object):
            def __init__(self, employee_id, dict, env):
                self.employee_id = employee_id
                self.dict = dict
                self.env = env

            def __getattr__(self, attr):
                return attr in self.dict and self.dict.__getitem__(attr) or 0.0

        class InputLine(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = fields.Date.today()
                self.env.cr.execute("""
                    SELECT sum(amount) as sum
                    FROM hr_payslip as hp, hr_payslip_input as pi
                    WHERE hp.employee_id = %s AND hp.state = 'done'
                    AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s""",
                                    (self.employee_id, from_date, to_date, code))
                return self.env.cr.fetchone()[0] or 0.0

        class WorkedDays(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def _sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = fields.Date.today()
                self.env.cr.execute("""
                    SELECT sum(number_of_days) as number_of_days, sum(number_of_hours) as number_of_hours
                    FROM hr_payslip as hp, hr_payslip_worked_days as pi
                    WHERE hp.employee_id = %s AND hp.state = 'done'
                    AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s""",
                                    (self.employee_id, from_date, to_date, code))
                return self.env.cr.fetchone()

            def sum(self, code, from_date, to_date=None):
                res = self._sum(code, from_date, to_date)
                return res and res[0] or 0.0

            def sum_hours(self, code, from_date, to_date=None):
                res = self._sum(code, from_date, to_date)
                return res and res[1] or 0.0

        class Payslips(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = fields.Date.today()
                self.env.cr.execute("""SELECT sum(case when hp.credit_note = False then (pl.total) else (-pl.total) end)
                            FROM hr_payslip as hp, hr_payslip_line as pl
                            WHERE hp.employee_id = %s AND hp.state = 'done'
                            AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pl.slip_id AND pl.code = %s""",
                                    (self.employee_id, from_date, to_date, code))
                res = self.env.cr.fetchone()
                return res and res[0] or 0.0

        # we keep a dict with the result because a value can be overwritten by another rule with the same code
        result_dict = {}
        rules_dict = {}
        worked_days_dict = {}
        inputs_dict = {}
        blacklist = []
        payslip = self.env['hr.payslip'].browse(payslip_id)
        for worked_days_line in payslip.worked_days_line_ids:
            worked_days_dict[worked_days_line.code] = worked_days_line
        for input_line in payslip.input_line_ids:
            inputs_dict[input_line.code] = input_line

        categories = BrowsableObject(payslip.employee_id.id, {}, self.env)
        inputs = InputLine(payslip.employee_id.id, inputs_dict, self.env)
        worked_days = WorkedDays(payslip.employee_id.id, worked_days_dict, self.env)
        payslips = Payslips(payslip.employee_id.id, payslip, self.env)
        rules = BrowsableObject(payslip.employee_id.id, rules_dict, self.env)

        baselocaldict = {'categories': categories, 'rules': rules, 'payslip': payslips, 'worked_days': worked_days,
                         'inputs': inputs}
        # get the ids of the structures on the contracts and their parent id as well
        # contracts = self.env['hr.contract'].browse(contract_ids)
        # structure_ids = contracts.get_all_structures()
        # get the rules of the structure and thier children
        # rule_ids = self.env['hr.payroll.structure'].browse(structure_ids).get_all_rules()
        # run the rules by sequence
        # sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x: x[1])]
        # sorted_rules = self.env['hr.salary.rule'].browse(sorted_rule_ids)

        # for contract in contracts:
        #     employee = contract.employee_id
        #     localdict = dict(baselocaldict, employee=employee, contract=contract)
        #     for rule in sorted_rules:
        #         key = rule.code + '-' + str(contract.id)
        #         localdict['result'] = None
        #         localdict['result_qty'] = 1.0
        #         # Adapting the salary amount according to the selected date period.
        #         if (rule.code == 'BASIC'):
        #             payslip.date_from = payslip.date_from.split(' ')[0]
        #             payslip.date_to = payslip.date_to.split(' ')[0]
        #             # d1 = date(int(payslip.date_from.split('-')[0]),
        #             #           int(payslip.date_from.split('-')[1]),
        #             #           int(payslip.date_from.split('-')[2]))  # start date, DANGER IF TIME FORMAT CHANGES
        #             d1 = fields.Date.from_string(payslip.date_from)
        #             # d2 = date(int(payslip.date_to.split('-')[0]),
        #             #           int(payslip.date_to.split('-')[1]),
        #             #           int(payslip.date_to.split('-')[2]))  # end date, DANGER IF TIME FORMAT CHANGES
        #             d2 = fields.Date.from_string(payslip.date_to)
        #             delta = str(d2 - d1).split(',')[0].split()[0]  # timedelta
        #             if delta in ['27', '28', '29', '30', '31']:  # approximate period to 30 days.
        #                 delta = 29  # biased in the nextline to 30.
        #             elif delta == '0:00:00':
        #                 delta = 0
        #             localdict['result_rate'] = ((int(
        #                 delta) + 1) / 30.0) * 100.0  # changing percentage according to the selected date period.
        #         else:
        #             localdict['result_rate'] = 100
        #         # localdict['result_rate'] = 100
        #         # check if the rule can be applied
        #         if rule.satisfy_condition(localdict) and rule.id not in blacklist:
        #             # compute the amount of the rule
        #             amount, qty, rate = rule.compute_rule(localdict)
        #             # check if there is already a rule computed with that code
        #             previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
        #             # set/overwrite the amount computed for this rule in the localdict
        #             tot_rule = amount * qty * rate / 100.0
        #             localdict[rule.code] = tot_rule
        #             rules_dict[rule.code] = rule
        #             # sum the amount for its salary category
        #             localdict = _sum_salary_rule_category(localdict, rule.category_id, tot_rule - previous_amount)
        #             # create/overwrite the rule in the temporary results
        #             result_dict[key] = {
        #                 'salary_rule_id': rule.id,
        #                 'contract_id': contract.id,
        #                 'name': rule.name,
        #                 'code': rule.code,
        #                 'category_id': rule.category_id.id,
        #                 'sequence': rule.sequence,
        #                 'appears_on_payslip': rule.appears_on_payslip,
        #                 'condition_select': rule.condition_select,
        #                 'condition_python': rule.condition_python,
        #                 'condition_range': rule.condition_range,
        #                 'condition_range_min': rule.condition_range_min,
        #                 'condition_range_max': rule.condition_range_max,
        #                 'amount_select': rule.amount_select,
        #                 'amount_fix': rule.amount_fix,
        #                 'amount_python_compute': rule.amount_python_compute,
        #                 'amount_percentage': rule.amount_percentage,
        #                 'amount_percentage_base': rule.amount_percentage_base,
        #                 'register_id': rule.register_id.id,
        #                 'amount': amount,
        #                 'employee_id': contract.employee_id.id,
        #                 'quantity': qty,
        #                 'rate': rate,
        #             }
        #         else:
        #             # blacklist this rule and its children
        #             blacklist += [id for id, seq in rule._recursive_search_of_rules()]
        return [value for code, value in result_dict.items()]

    # @api.model
    # def get_contract(self, employee, date_from, date_to):
    #
    #     contracts = self.env['hr.contract'].search([('employee_id', '=', employee.id), ('state', '=', 'open')]).ids
    #     return contracts

    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):
        import time
        from datetime import datetime, timedelta
        import babel

        if (not self.employee_id) or (not self.date_from) or (not self.date_to):
            return

        employee = self.employee_id
        date_from = self.date_from
        date_to = self.date_to

        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(date_from, "%Y-%m-%d")))
        locale = self.env.context.get('lang') or 'en_US'
        self.name = _('Salary Slip of %s for %s') % (
            employee.name, tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale)))
        self.company_id = employee.company_id

        # contract_ids = self.env['hr.contract']
        # if not self.env.context.get('contract') or not self.contract_id:
            # contract_ids = self.get_contract(employee, date_from, date_to)
            # contract_ids = self.env['hr.contract'].search(
            #     [('employee_id', '=', self.employee_id.id), ('state', '=', 'open')])  # .ids
        #     if not contract_ids:
        #         return
        #     self.contract_id = self.env['hr.contract'].browse(contract_ids[0].id)
        #
        # if not self.contract_id.struct_id:
        #     return
        # self.struct_id = self.contract_id.struct_id

        # computation of the salary input
        # worked_days_line_ids = self.get_worked_day_lines(contract_ids, date_from, date_to)
        worked_days_lines = self.worked_days_line_ids.browse([])
        # for r in worked_days_line_ids:
        #     worked_days_lines += worked_days_lines.new(r)
        self.worked_days_line_ids = worked_days_lines

        # input_line_ids = self.get_inputs(contract_ids, date_from, date_to)
        input_lines = self.input_line_ids.browse([])
        # for r in input_line_ids:
        #     input_lines += input_lines.new(r)
        self.input_line_ids = input_lines
        return


class NotifyMessage(models.Model):
    _inherit = 'mail.message'

    def notify_user_attend(self, employee, date, custom_in, custom_out):
        try:
            user = self.env["hr.employee"].browse(employee)
        except Exception as e:
            pass

        template_obj = self.env['mail.template'].sudo().search([('name', '=', 'Attendance Notification')], limit=1)
        body = template_obj.body_html

        date = str(date).split()[0]
        send_mail = self.env['ir.mail_server'].search([])

        body = "Dear " + user.lastname + " " + user.firstname + ', <br>' + "We would notify you " + "in " + date + " " + "your check in is " + custom_in + '<br>' + "and your check out is " + " " + custom_out
        mail_values = {
            'subject': "Attendance notification",
            'body_html': body,
            'email_to': user.work_email,
            'email_from': send_mail.smtp_user  # template_obj.email_from,
        }
        self.env['mail.mail'].create(mail_values).send()
