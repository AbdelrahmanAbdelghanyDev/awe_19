# -*- coding: utf-8 -*-

import logging
from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class HrHolidayStatus(models.Model):
    _name = 'hr.holidays.status'

    is_annual_leave = fields.Boolean('Annual Leave?')
    days_before = fields.Float('Days Before', help="Days before, that does't allow leaves after this number of days.")
    days_after = fields.Float('Days After', help="Days after, that does't allow leaves after this number of days.")

    # @api.model
    # def _action_cron(self):
    #     types = self.search([('is_annual_leave', '=', True)])
    #     today = fields.Date.from_string(fields.Date.today())
    #     date_start_3_months_before = (datetime.now() + relativedelta(months=-3)).date()
    #     contracts = self.env['hr.contract'].search(
    #         [('vacation', '!=', False), ('date_start', '<=', date_start_3_months_before)])
    #     for contract in contracts:
    #
    #         for type in types:
    #             holiday = self.env['hr.holidays'].search([('state', '=', 'validate'), ('holiday_type', '=', 'employee'),
    #                                                       ('employee_id', '=', contract.employee_id.id),
    #                                                       ('holiday_status_id', '=', type.id)], limit=1)
    #             create_date = False
    #             if holiday:
    #                 create_date = fields.Datetime.from_string(holiday.create_date).date()
    #             if contract.vacation == 1:
    #                 number_of_days = 21
    #             elif contract.vacation == 2:
    #                 number_of_days = 30
    #
    #             if not create_date or (create_date and create_date.year != today.year):
    #                 holiday = self.env['hr.holidays'].create({
    #                     'name': "Auto leave allocation %s" % today.year,
    #                     'type': 'add',
    #                     'holiday_type': 'employee',
    #                     'employee_id': contract.employee_id.id,
    #                     'holiday_status_id': type.id,
    #                     'number_of_days_temp': number_of_days,
    #
    #                 })
    #                 holiday.action_approve()


class Holidays(models.Model):
    _name = 'hr.holidays'

    date_from_alloca = fields.Datetime('From')
    date_to_alloca = fields.Datetime('to')

    # @api.multi
    def _check_security_action_refuse(self):
        if not (self.env.user.has_group('hr_holidays.group_hr_holidays_user') or self.env.user.has_group(
                'hr_holidays_awe.group_hr_holidays_first')):
            raise UserError(_('Only an HR Officer or Manager can refuse leave requests.'))

    # @api.multi
    def _check_security_action_approve(self):
        if not (self.env.user.has_group('hr_holidays.group_hr_holidays_user') or self.env.user.has_group(
                'hr_holidays_awe.group_hr_holidays_first')):
            raise UserError(_('Only an HR Officer or Manager can approve leave requests.'))

    # @api.multi
    def _check_security_action_validate(self):
        if not (self.env.user.has_group('hr_holidays.group_hr_holidays_user') or self.env.user.has_group(
                'hr_holidays_awe.group_hr_holidays_first')):
            raise UserError(_('Only an HR Officer or Manager can approve leave requests.'))

    def _check_state_access_right(self, vals):
        if vals.get('state') and vals['state'] not in ['draft', 'confirm', 'cancel'] and not (
                self.env.user.has_group('hr_holidays.group_hr_holidays_user') or self.env.user.has_group(
            'hr_holidays_awe.group_hr_holidays_first')):
            return False
        return True

    # @api.multi
    def action_validate(self):
        self._check_security_action_validate()

        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        for holiday in self:
            if holiday.state not in ['confirm', 'validate1','first_approval']:
                raise UserError(_('Leave request must be confirmed in order to approve it.'))
            if holiday.state == 'first_approval' and not holiday.env.user.has_group('custom_hr_leaves.leave_second_approvers'):
                raise UserError(_('Only an HR Manager can apply the second approval on leave requests.'))

            holiday.write({'state': 'validate'})
            if holiday.double_validation:
                holiday.write({'second_approver_id': current_employee.id})
            else:
                holiday.write({'first_approver_id': current_employee.id})
            if holiday.holiday_type == 'employee' and holiday.type == 'remove':
                holiday.sudo()._validate_leave_request()
            elif holiday.holiday_type == 'category':
                leaves = self.env['hr.holidays']
                for employee in holiday.category_id.employee_ids:
                    values = holiday._prepare_create_by_category(employee)
                    leaves += self.with_context(mail_notify_force_send=False).create(values)
                # TODO is it necessary to interleave the calls?
                leaves.action_approve()
                if leaves and leaves[0].double_validation:
                    leaves.action_validate()
        return True

    @api.onchange('date_to_alloca')
    def onch_name(self):
        if self.date_from_alloca and self.date_to_alloca:
            d1 = datetime.strptime(self.date_from_alloca, "%Y-%m-%d %H:%M:%S")
            d2 = datetime.strptime(self.date_to_alloca, "%Y-%m-%d %H:%M:%S")
            self.number_of_days_temp = abs((d2 - d1).days)

    @api.constrains('date_from', 'date_to', 'holiday_status_id')
    def _check_boundaries(self):
        if self.date_from and self.holiday_status_id and self.holiday_status_id:
            today = date.today()
            date_from = fields.Datetime.from_string(self.date_from).date()
            if today < date_from:
                if self.holiday_status_id.days_before and (
                        date_from - today).days <= self.holiday_status_id.days_before:
                    raise UserError(
                        _('You cannot apply leaves on this type %s days before.' % self.holiday_status_id.days_before))
            else:
                if self.holiday_status_id.days_after and (today - date_from).days >= self.holiday_status_id.days_after:
                    raise UserError(
                        _('You cannot apply leaves on this type %s days after.' % self.holiday_status_id.days_after))
