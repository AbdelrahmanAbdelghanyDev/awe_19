# -*- coding: utf-8 -*-
import pytz
import sys
from datetime import timedelta, time, date
from datetime import datetime
try:
    from zk import ZK
    sys.path.append("zk")
except ImportError:
    pass

from odoo import api, fields, models
import math

class HrAttendanceWorkingHours(models.Model):
    _inherit = 'resource.calendar.attendance'

    late_in = fields.Float('Late In')
    early_out = fields.Float('Early Out')


class HrAttendanceDay(models.Model):
    _inherit = 'hr.attendance'

    day_name = fields.Char('Day')
    late_x = fields.Float('Late')
    early_x = fields.Float('Early')
    work_time_x = fields.Float('Scheduled working time')

    @api.constrains('check_in','check_out')
    def const_chin(self):
        working_hours_rule = self.env['resource.calendar'].search([('id','=',self.employee_id.resource_calendar_id.id)]).attendance_ids
        if self.check_in:
            # print(self.check_in.time())
            # print(float(datetime.strftime(self.check_in, "%H.%M")))
            # print('====')
            self.day_name = self.check_in.date().strftime("%A")
            if self.day_name == "Sunday":
                x = '6'
            if self.day_name == "Monday":
                x = '0'
            if self.day_name == "Tuesday":
                x = '1'
            if self.day_name == "Wednesday":
                x = '2'
            if self.day_name == "Thursday":
                x = '3'
            if self.day_name == "Friday":
                x = '4'
            if self.day_name == "Saturday":
                x = '5'
            for rule in working_hours_rule:
                if x == rule.dayofweek:
                    frac, whole = math.modf(float(datetime.strftime(self.check_in + timedelta(hours=2), "%H.%M")))
                    ch_in = round(whole + ((round(frac, 2)/60)*100), 2)
                    if ch_in > rule.late_in:
                        self.late_x = ch_in - rule.hour_from

                    if self.check_out:
                        frac_out, whole_out = math.modf(float(datetime.strftime(self.check_out + timedelta(hours=2), "%H.%M")))

                        ch_out = round(whole_out + ((round(frac_out, 2)/60)*100),2)

                        if ch_in <= rule.hour_from and ch_out >= rule.hour_to: # geh badry w meshy mt25r
                            self.work_time_x = rule.hour_to - rule.hour_from

                        if ch_in > rule.hour_from and ch_out > rule.hour_to: # geh mt25r w mshy mt2r
                            self.work_time_x = rule.hour_to - ch_in

                        if ch_in <= rule.hour_from and ch_out < rule.hour_to: # geh badry w meshy badry
                            self.work_time_x = ch_out - rule.hour_from

                        if ch_in > rule.hour_from and ch_out < rule.hour_to: # geh mt2r w meshy badry
                            self.work_time_x = ch_out - ch_in

                        if ch_out < rule.early_out:
                            self.early_x = rule.early_out - ch_out

