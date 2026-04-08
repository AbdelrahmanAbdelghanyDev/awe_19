# -*- coding: utf-8 -*-
import pytz
import sys
from datetime import timedelta, time, date
import datetime
try:
    from zk import ZK
    sys.path.append("zk")
except ImportError:
    pass

from odoo import api, fields, models
from odoo import _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    device_id = fields.Char(string='Biometric Device ID')

    # def _check_validity(self):
    #     return


class ZkMachineEmployee(models.Model):
    _inherit = 'hr.employee'

    emp_Shift = fields.Boolean(string='Shift', default=False)
    Check_in_from = fields.Char(string='Check_in')
    Check_in_to = fields.Char()
    Check_out_from = fields.Char(string='Check_out')
    Check_out_to = fields.Char()


class ZkMachine(models.Model):
    _name = 'zk.machine'

    name = fields.Char(string='Machine IP', required=True)
    port_no = fields.Integer(string='Port No', required=True)
    ping_machine = fields.Boolean(string='Ping',default=False)
    password_machine = fields.Char(string='Machine Password')
    udp_machine = fields.Boolean(string='UDP',default=False)
    address_id = fields.Many2one('res.partner', string='Working Address')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)
    attendance_days = fields.Integer(string='Attendance Days', help="""Download the last (Attendance Days)""")
    att_type = fields.Selection([('in_out', 'Use In / Out'),('filo', 'Use First / Last')], string='Attendance Type', default='in_out')
    type = fields.Selection([('machine', 'Machine'), ('db', 'Database')], string='Connection Type', default='machine')
    interval = fields.Integer('Interval')

    #@api.onchange('interval')
    #def change_interval(self):
    #    if self.interval:
    #        self.env['ir.cron'].sudo().search([('name','=','Download Attendance Data')]).write({'interval_number': self.interval})


    def device_connect(self, zk):
        try:
            conn = zk.connect()
            if conn:
                connection = True
            else:
                connection = False
        except:
            connection = False
        zk.disconnect()
        return connection

    #
    # def clear_attendance(self):
    #     mac_obj = self.env['zk.machine'].search([])
    #     for info in mac_obj:
    #         machine_ip = info.name
    #         port = info.port_no
    #         ping = info.ping_machine
    #         password = info.password_machine
    #         udp = info.udp_machine
    #         zk = ZK(machine_ip, port,password=password, force_udp=udp, ommit_ping=ping)
    #         conn = zk.connect()
    #         if conn:
    #             clear_data = conn.get_attendance()
    #             if clear_data:
    #                 conn.clear_attendance()
    #             else:
    #                 raise UserError(_('Unable to get the attendance log, please try again later.'))
    #         else:
    #             raise UserError(_('Unable to connect, please check the parameters and network connections.'))

    def zkgetuser(self, zk):
        conn = zk.connect()
        users = conn.get_users()
        dict_users = {}
        if users:
            for user in users:
                dict_users[user.user_id] = user.user_id, user.name, user.privilege, user.password
            zk.disconnect()
            return dict_users
        else:
            return False

    def zkgetatten(self, zk):
        conn = zk.connect()
        atten = conn.get_attendance()
        dict_atten = []
        days = timedelta(days=self.attendance_days)
        date_now = datetime.datetime.now().date()
        res = date_now - days
        if atten:
            for rec in atten:
                if not self.attendance_days or self.attendance_days == 0:
                    dict_atten.append((rec.user_id, rec.timestamp, rec.punch, rec.status))
                else:
                    if str(rec.timestamp) > str(res):
                        dict_atten.append((rec.user_id, rec.timestamp, rec.punch, rec.status))
            zk.disconnect()
            return dict_atten
        else:
            return False

    def download_attendance(self):
        if self.type == 'machine':
            zk_attendance = self.env['zk.machine.attendance']
            att_obj = self.env['hr.attendance']
            mac_obj = self.env['zk.machine'].search([])
            for info in mac_obj:
                machine_ip = info.name
                port = info.port_no
                ping = info.ping_machine
                password = info.password_machine
                udp = info.udp_machine
                zk = ZK(machine_ip, port,  password=password, force_udp=udp, ommit_ping=ping)
                conn = self.device_connect(zk)
                print(conn)
                if conn:
                    attendance = self.zkgetatten(zk)
                    user = self.zkgetuser(zk)
                    if attendance:

                        for each in attendance:
                            # print(each)
                            atten_time = each[1]
                            atten_time = datetime.datetime.strptime(
                                atten_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                            local_tz = pytz.timezone(
                                self.env.user.partner_id.tz or 'Africa/Cairo')
                            local_dt = local_tz.localize(atten_time, is_dst=None)
                            utc_dt = local_dt.astimezone(pytz.utc)
                            utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                            atten_time = datetime.datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")
                            atten_time = fields.Datetime.to_string(atten_time)
                            if user:
                                for uid in user:

                                    if user[uid][0] == each[0]:
                                        get_user_id = self.env['hr.employee'].search([('device_id', '=', str(each[0]))])
                                        if get_user_id:
                                            duplicate_atten_ids = zk_attendance.search(
                                                [('device_id', '=', str(each[0])), ('punching_time', '=', atten_time)])
                                            if duplicate_atten_ids:
                                                continue
                                            else:
                                                zk_attendance.create({'employee_id': get_user_id.id,
                                                                      'device_id': str(each[0]),
                                                                      'punch_type': str(each[2]),
                                                                      'punching_time': atten_time,
                                                                      'address_id': info.address_id.id})

                                        else:
                                            employee = self.env['hr.employee'].create({'device_id': str(each[0]), 'name': user[uid][1]})
                                            zk_attendance.create({'employee_id': employee.id,
                                                                  'device_id': each[0],
                                                                  'punch_type': str(each[2]),
                                                                  'punching_time': atten_time,
                                                                  'address_id': info.address_id.id})

                                    else:
                                        pass
                        employees = []
                        day = timedelta(days=1)
                        hours = timedelta(hours=2)
                        records_log = self.env['zk.machine.attendance'].search([])
                        for rec in records_log:
                            if rec.employee_id.device_id not in employees:
                                employees.append(rec.employee_id.device_id)
                        #records_employee = ['21', '8', '22', '12', '11', '100', '20', '1', '9', '200', '6']
                        if self.att_type == 'filo':

                            for one_employee in employees:
                                record_employee = []
                                att_emp = self.env['zk.machine.attendance'].search([('device_id','=',one_employee)])
                                # print(att_emp)
                                if att_emp not in record_employee:
                                    record_employee.append(att_emp)
                                # print(record_employee)
                                for x in record_employee:
                                    date_empl = []
                                    for y in x:

                                        date_empl.append(y.punching_time)
                                    # min_date = (min(date_empl)).strftime("%Y-%m-%d")
                                    min_date = (datetime.datetime.strptime(min(date_empl), '%Y-%m-%d %H:%M:%S')).date()
                                    max_date = (datetime.datetime.strptime(max(date_empl), '%Y-%m-%d %H:%M:%S')).date()
                                    # max_date = (max(date_empl)).strftime("%Y-%m-%d")
                                    # print(min_date)
                                    # print(max_date)
                                    while min_date <= max_date:
                                        equal_time = []
                                        for rec_for_emp in att_emp:
                                            # if min_date == rec_for_emp.punching_time.date():
                                            if min_date == (datetime.datetime.strptime(rec_for_emp.punching_time, '%Y-%m-%d %H:%M:%S')).date():
                                                equal_time.append(rec_for_emp.punching_time)
                                        if equal_time:
                                            # print(rec_for_emp.punching_time)
                                            # print(equal_time)
                                            hr_att = att_obj.search(
                                                [('employee_id', '=', rec_for_emp.employee_id.id),('check_out', '=', False)])
                                            if not hr_att:
                                                att_obj.search([('employee_id', '=', rec_for_emp.employee_id.id),
                                                                ('check_in', '=', min(equal_time))]).unlink()
                                                att_obj.create({'employee_id': rec_for_emp.employee_id.id, 'check_in': min(equal_time),'check_out': max(equal_time)})
                                            if hr_att:

                                                hr_att.write({'check_out': hr_att.check_in})
                                                    # print(hr_att)
                                        min_date = min_date + day

                        if self.att_type == 'in_out':

                            for one_employee in employees:
                                att_emp = self.env['zk.machine.attendance'].search([('device_id','=',one_employee)],order='punching_time')
                                # print(one_employee)

                                for rec in att_emp:
                                    duplicate_att = att_obj.search([('employee_id', '=', rec.employee_id.id),('check_in', '=', rec.punching_time)])
                                    duplicate_att_2 = att_obj.search([('employee_id', '=', rec.employee_id.id),('check_out', '=', rec.punching_time)])
                                    # print('1',duplicate_att)
                                    # print('2',duplicate_att_2)
                                    if duplicate_att or duplicate_att_2:
                                        # print('dupl')
                                        continue
                                    else:
                                        # print(rec.punching_time)
                                        # print(rec.punch_type)

                                        hr_att = att_obj.search([('employee_id', '=', rec.employee_id.id), ('check_in', '!=', False), ('check_out', '=', False)])

                                        if hr_att and rec.punch_type == '1':
                                            # print('3333')
                                            hr_att.write({'check_out': rec.punching_time})

                                        if hr_att and rec.punch_type == '0':
                                            # print('2222')
                                            hr_att.write({'check_out': hr_att.check_in})
                                            att_obj.create({'employee_id': rec.employee_id.id, 'check_in': rec.punching_time})

                                        if (not hr_att) and rec.punch_type == '0':
                                            # print('test')
                                            att_obj.create({'employee_id': rec.employee_id.id, 'check_in': rec.punching_time})

                                        if (not hr_att) and rec.punch_type == '1':
                                            # print('test2')
                                            att_obj.create({'employee_id': rec.employee_id.id, 'check_in': rec.punching_time , 'check_out': rec.punching_time})
                                        else:
                                            pass
                                # print('------')

                        return True



                    else:
                        raise UserError(_('Unable to get the attendance log, please try again later.'))
                else:
                    raise UserError(_('Unable to connect, please check the parameters and network connections.'))
        if self.type == 'db':
            zk_attendance = self.env['zk.machine.attendance']
            att_obj = self.env['hr.attendance']
            cursor = self.db_connect()
            days_before_60 = datetime.combine(date.today(), time.min) + relativedelta(days=-60)
            yesterday = datetime.combine((date.today() - timedelta(days=1)), time.max)
            tsql = "SELECT UserID, VerifyMode, InOutMode, LogDateTime, MachineIP from Att_Log_Table_Temp where LogDateTime <= ?;"
            # min_ = datetime.combine((date.today().replace(day=10)), time.min)
            # max_ = datetime.combine((date.today().replace(day=10)), time.max)
            # tsql = "SELECT UserID, VerifyMode, InOutMode, LogDateTime, MachineIP from Att_Log_Table_Temp where LogDateTime >= ? and LogDateTime <= ?;"
            # with cursor.execute(tsql, min_, max_):
            # with cursor.execute(tsql, yesterday):
            #     row = cursor.fetchone()
            #     while row:
            cursor.execute(tsql, (days_before_60, yesterday))
            for row in cursor:
                if row:
                    # sn          UserID      VerifyMode  InOutMode   LogDateTime             MachineIP
                    # (873, VerifyMode,  0, datetime.datetime(2018, 9, 6, 17, 10, 48), '10.10.2.40')
                    try:
                        atten_time = row[3]
                        atten_time = datetime.strptime(atten_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                        local_tz = pytz.timezone(self.env.user.partner_id.tz or 'GMT')
                        local_dt = local_tz.localize(atten_time, is_dst=None)
                        utc_dt = local_dt.astimezone(pytz.utc)
                        utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                        atten_time = datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")
                        atten_time = fields.Datetime.to_string(atten_time)
                    except:
                        print('AmbiguousTimeError')

                    get_user_id = self.env['hr.employee'].search([('device_id', '=', str(row[0]))])
                    if get_user_id:
                        duplicate_atten_ids = zk_attendance.search(
                            [('device_id', '=', str(row[0])), ('punching_time', '=', atten_time)])
                        if duplicate_atten_ids:
                            continue
                        else:
                            zk_attendance.create({'employee_id': get_user_id.id,
                                                  'device_id': row[0],
                                                  'attendance_type': str(row[1]),
                                                  'punch_type': str(row[2]),
                                                  'punching_time': atten_time,
                                                  'address_id': self.address_id.id})
                            self.create_attendance_record(get_user_id, atten_time, row[2])
                    else:
                        employee = self.env['hr.employee'].create({'device_id': str(row[0]), 'name': row[0]})
                        zk_attendance.create({'employee_id': employee.id,
                                              'device_id': row[0],
                                              'attendance_type': str(row[1]),
                                              'punch_type': str(row[2]),
                                              'punching_time': atten_time,
                                              'address_id': self.address_id.id})
                        att_obj.create({'employee_id': employee.id, 'check_in': atten_time, 'check_out': atten_time})

    #@api.model
    #def cron_download(self):
    #    machines = self.env['zk.machine'].search([])
    #    for machine in machines:
    #        machine.download_attendance()

