# -*- coding: utf-8 -*-
import math
import base64

from werkzeug import urls

from odoo import fields, tools, _
from odoo.exceptions import ValidationError
from odoo.http import Controller, request, route, Response
from datetime import datetime, timedelta, time
from odoo.exceptions import UserError, AccessError, ValidationError


class LeavePortal(Controller):

    # all leaves page
    @route(['/my/leaves'], type='http', auth="user", website=True)
    def myLeaves(self, **kw):
        def convert_datetime_to_date(date):
            if date:
                date = datetime.strptime(str(date).split(' ')[0], '%Y-%m-%d')
                return date.strftime("%m/%d/%Y")
            else:
                return False

        get_class_state_dict = {'refuse': 'label label-danger', 'confirm': 'label label-info',
                                'validate1': 'label label-success', 'draft': 'label label-warning',
                                'cancel': 'label label-default', 'validate': 'label label-success'}
        get_description_state_dict = {'draft': "To Submit", 'cancel': 'Cancelled',
                                      'confirm': 'To Approve',
                                      'refuse': 'Refused', 'validate': 'Approved', 'validate1': 'Second Approval'}
        vals = {}
        vals['convert_datetime_to_date'] = convert_datetime_to_date
        vals['get_description_state_dict'] = get_description_state_dict
        vals['get_class_state_dict'] = get_class_state_dict

        # get employee has the current user as related user
        employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', request.uid)])

        # get leave types
        leaves = {}
        types = request.env['hr.leave.type'].sudo().search([('name', 'in', [])])

        # get leaves for these leave types
        if employee_id:
            leaves = request.env['hr.leave'].sudo().search(
                [('employee_id', '=', employee_id.id),
                 ('holiday_status_id', 'not in', types.ids)])
        vals['leaves'] = leaves

        return request.render("portal_leave.my_leaves", vals)

    @route(['/my/leave/create'], type='http', auth="user", website=True)
    def myLeavesCreate(self, vals={}, **kw):
        if 'error' not in vals:
            vals['error'] = {}

        types = request.env['hr.leave.type'].sudo().search([('name', 'in', [])])
        vals['holiday_status_ids'] = request.env['hr.leave.type'].sudo().search([('id', 'not in', types.ids)])

        employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.uid)]).id

        for h_s in vals['holiday_status_ids']:
            # get some fields to be shown "format/shape of leave types"
            h_s._compute_leaves_portal()
            h_s.display_name = h_s.name_get_portal()[0][1]
            h_s.name_get()

        return request.render("portal_leave.my_leave", vals)

    @route(['/my/leave/<int:leave_id>'], type='http', auth="user", website=True)
    def myLeave(self, leave_id=0, **kw):
        def convert_datetime_to_date(date):
            if date:
                date = datetime.strptime(str(date).split(' ')[0], '%Y-%m-%d')
                return date.strftime("%m/%d/%Y")
            else:
                return False

        vals = {}
        vals['error'] = {}
        vals['convert_datetime_to_date'] = convert_datetime_to_date
        vals['holiday_status_ids'] = request.env['hr.leave.type'].sudo().search([])

        if leave_id > 0:
            vals['leave'] = request.env['hr.leave'].sudo().browse(leave_id)
        return request.render("portal_leave.my_leave", vals)

    def send_email_to_approvers(self, employee_id, email_to):

        body = '''
                Dear,<br>
                <pre>
        Kindly noted that Employee {employee} Requested a leave, Waiting for your approval.
                <br>
                Best Regards,
                </pre>'''.format(employee=employee_id.display_name, )
        mail_server = request.env['ir.mail_server'].sudo().search([], limit=1)
        mail_values = {
            'subject': "Leave Request Notification",
            'body_html': body,
            'email_to': email_to,
            'email_from': mail_server.smtp_user
        }
        approval_mail = request.env['mail.mail'].sudo().create(mail_values)
        approval_mail.sudo().send()

    def create_leave_attachment(self, attachment):
        #
        partner = request.env.user.partner_id

        Attachments = request.env['ir.attachment'].sudo()

        name = attachment.filename

        file = attachment

        attachment_id = Attachments.sudo().create({

            'name': name,

            'type': 'binary',

            'datas': base64.b64encode(file.read()),

            'res_model': 'hr.leave',

            'res_id': partner.id

        })
        return attachment_id.id

    #
    def _check_dates_constrains(self, holiday_status_id, request_date_from, employee_id, number_of_days):
        if holiday_status_id.type == 'conflict':
            has_time_off = request.env['hr.leave'].sudo().search(
                [
                    '|',
                    ('date_month_start', '=',
                     datetime.strptime(str(request_date_from), '%Y-%m-%d').strftime('%m')),
                    ('date_month_end', '=',
                     datetime.strptime(str(request_date_from), '%Y-%m-%d').strftime('%m')),
                    '|',
                    ('date_year_start', '=',
                     datetime.strptime(str(request_date_from), '%Y-%m-%d').strftime('%Y')),
                    ('date_year_end', '=',
                     datetime.strptime(str(request_date_from), '%Y-%m-%d').strftime('%Y')),
                    ('employee_ids', 'in', [employee_id.id]), ('state', '=', 'validate'),
                    ('holiday_status_id.type', '=', 'conflict')
                ])
            has_time_off = has_time_off.mapped('number_of_days')
            has_time_off = sum(has_time_off)
            if (has_time_off + number_of_days) > 2:
                raise ValidationError(_('You can\'t select more than two days in the same month'))
            else:
                pass

        elif holiday_status_id.type == 'put':
            date_end_o = fields.Datetime.from_string(request_date_from)
            date_start_o = fields.Datetime.from_string(employee_id.hire_date)
            # delta = relativedelta.relativedelta(date_end_o, date_start_o)

            if date_end_o and date_start_o:
                delta = date_end_o - date_start_o
                delta_months = delta.days / 30
                if delta_months <= 10:
                    raise ValidationError(_('The hiring date for emp is less than 10 months'))

    #
    @route(['/my/leave/update'], type='http', auth="user", website=True)
    def myLeaveUpdate(self, leave_id, **post):

        holiday_type = request.env['hr.leave.type'].sudo().search([('id', '=', int(post['holiday_status_id']))])
        # if support document true for leave type,must add attachment

        # some paramters for half day leaves
        # if post['request_date_from_period'] != '':
        #     # check if selected holiday type is support half day or not
        #     if holiday_type.request_unit != 'half_day':
        #         request._cr.rollback()
        #         post['error_message'] = "this leave type not support half day!"
        #         return self.myLeavesCreate(post)
        #
        #     post['date_to'] = post['date_from']
        #     post['request_unit_half'] = True

        if leave_id != '':
            leave_id = int(leave_id)
            if leave_id > 0:
                leave_id = request.env['hr.leave'].sudo().browse(leave_id)
                if leave_id and 'delete_btn' in post and leave_id.state == 'draft':
                    leave_id.unlink()
                elif leave_id:
                    post['number_of_days'] = (
                            datetime.strptime(post['date_to'], "%m/%d/%Y") - datetime.strptime(post['date_from'],
                                                                                               "%m/%d/%Y")).days
                    post['date_from'] = datetime.strptime(post['date_from'], "%m/%d/%Y").strftime("%Y-%m-%d %H:%M:%S")
                    post['date_to'] = datetime.combine(datetime.strptime(post['date_to'], "%m/%d/%Y").date(),
                                                       time(21, 0, 0)).strftime("%Y-%m-%d %H:%M:%S")
                    # # post['duration'] = post['date_to'] - post['date_from'] + 1
                    # if 'date_from_half_day' in post:
                    #     del post['date_from_half_day']
                    # if 'date_to_half_day' in post:
                    #     del post['date_to_half_day']

                    post['holiday_status_id'] = int(post['holiday_status_id'])
                    post['request_date_from'] = post['date_from']
                    post['request_date_to'] = post['date_to']
                    post['holiday_type'] = 'employee'
                    post['state'] = leave_id.state
                    leave_id.update({'date_to': post['date_to'],'date_from': post['date_from']})
                    leave_id.update(post)

                    leave_id._compute_date_from_to()
                    leave_id.update({'state': post['state']})
                    # if post['request_date_from_period'] != '':
                    #     leave_id.update({'request_unit_half': True})
                    #
                    # create attachment if passed
                    #
                    #


        else:
            post['number_of_days'] = (
                                             datetime.strptime(post['date_to'], "%m/%d/%Y") - datetime.strptime(
                                         post['date_from'],
                                         "%m/%d/%Y")).days + 1
            employee_id = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.uid)])
            post['employee_id'] = employee_id.id
            # post['chk_casual_leave'] = False
            # if post['employee_id'] is None:
            # post['employee_id'] = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.uid)]).id
            # post['project_id'] = request['project_id']
            print(post)
            try:
                post['holiday_status_id'] = int(post['holiday_status_id'])
                post['date_from'] = datetime.strptime(post['date_from'], "%m/%d/%Y").strftime("%Y-%m-%d %H:%M:%S")
                post['date_to'] = datetime.combine(datetime.strptime(post['date_to'], "%m/%d/%Y").date(),
                                                   time(21, 0, 0)).strftime("%Y-%m-%d %H:%M:%S")
                post['request_date_from'] = post['date_from']
                post['request_date_to'] = post['date_to']
                post['state'] = 'draft'
                post['holiday_type'] = 'employee'
                # del post['date_from']
                # del post['date_to']
                # check some constrains
                # self._check_dates_constrains(holiday_type,post['request_date_from'],employee_id,post['number_of_days'])
                leave_id = request.env['hr.leave'].sudo().create(post)

                leave_id.write({'state': 'draft'})
                # if post['request_date_from_period'] != '':
                #     leave_id.write({'request_unit_half': True})

                # create attachment if passed
                # attachment_id=self.create_leave_attachment(attachment)
                # leave_id.update({'supported_attachment_ids': [(6, 0, [attachment_id])]})

                #

                leave_id._compute_date_from_to()

                # send mail to leaves approve responsible persons
                # 1- for manager of the employee
                # self.send_email_to_approvers(leave_id.employee_id,leave_id.employee_id.parent_id.work_email)
                # #2- for second approval group
                # approvers= request.env.ref('portal_leave.leave_second_approvers').sudo().users
                # approvers = approvers.mapped('email')
                # for approver_user in approvers:
                #     self.sudo().send_email_to_approvers(leave_id.employee_id, approver_user)

                # leave_id._onchange_date_from()
            except Exception as exc:
                request._cr.rollback()
                post['error_message'] = "Error " + str(exc) + ' '
                return self.myLeavesCreate(post)
                # pass
                # return request.redirect('/my/leaves')
        return request.redirect('/my/leaves')

    @route(['/my/leave/delete'], type='http', auth="user", website=True)
    def myLeaveDelete(self, **post):
        for key, value in post.items():
            if key.isdigit():
                leave_id = int(key)
                leave_id = request.env['hr.leave'].sudo().browse(leave_id)
                if leave_id:
                    leave_id.sudo().unlink()
        return request.redirect('/my/leaves')
