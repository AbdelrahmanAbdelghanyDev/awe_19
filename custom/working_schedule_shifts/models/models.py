# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    month_ids = fields.One2many('calendar.month', 'resource_calendar_id', string='Calendar Month')


class CalendarMonth(models.Model):
    _name = "calendar.month"

    month = fields.Selection([
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December')
        ], 'Calendar Month', required=True)
    # fields.Date("Calendar Month")
    is_created = fields.Boolean(default=False, hidden_field=True)
    resource_calendar_id = fields.Many2one('resource.calendar', hidden_field=True)
    shift_ids = fields.One2many("calendar.month.day", "calendar_month_id", string="Day Shift")

    @api.model
    def create(self, vals):
        record = super(CalendarMonth, self).create(vals)
        print(vals, " ", self," ", record.id)
        print("inside create", self.shift_ids, (len(self.shift_ids) == 0), ' ',self.id, self.month, (self.month in range(1, 12)))
        calendar_month_day = self.env['calendar.month.day']
        if len(record.shift_ids) == 0 and record.month:
            current_year = date.today().year  # fields.Date.today().year
            month = int(record.month)
            print(type(current_year), type(record.month), type(month))
            month_start = date(current_year, month, 1)
            if month == 12:
                next_month_start = date(current_year + 1, 1, 1)
            else:
                next_month_start = date(current_year, month + 1, 1)
            days_in_month = (next_month_start - month_start).days
            print("start ", month_start, " next mon ", next_month_start, " days : ", days_in_month)
            print("self id ", self)
            for i in range(1, days_in_month+1):
                print(date(current_year, month, i))
                calendar_month_day.create({
                    'day': date(current_year, month, i),
                    'calendar_month_id': record.id,
                })
            record.is_created = True
        return record

    def button_day_details(self):
        view = {
            'name': 'Details',
            'view_mode': 'form',
            'res_model': 'calendar.month',
            'view_id': False,#'calendar_month_day_form_view',
            'type': 'ir.actions.act_window',#'ir.actions.act_window_close',
            'target': 'new',
            #'readonly': True,
            'res_id': self.id,
        }
        return view
    # @api.onchange('month')
    # def _onchange_month(self):
    #     # set auto-changing field
    #     print("inside onchange", self.shift_ids, (len(self.shift_ids) == 0), ' ', (self.month in range(1, 12)))
    #     calendar_month_day = self.env['calendar.month.day']
    #     if len(self.shift_ids) == 0 and self.month:
    #         current_year = date.today().year#fields.Date.today().year
    #         month = int(self.month)
    #         print(type(current_year), type(self.month), type(month))
    #         month_start = date(current_year, month, 1)
    #         if month == 12:
    #             next_month_start = date(current_year+1, 1, 1)
    #         else:
    #             next_month_start = date(current_year, month+1, 1)
    #         days_in_month = (next_month_start - month_start).days
    #         print("start ", month_start, " next mon ", next_month_start, " days : ", days_in_month)
    #         print("self id ", self)
    #         for i in range(1, days_in_month+1):
    #             print(date(current_year, month, i))
    #             calendar_month_day.create({
    #                 'day': date(current_year, month, i),
    #                 'calendar_month_id': self.id,
    #             })


class CalendarMonthDay(models.Model):
    _name = 'calendar.month.day'

    day = fields.Date("Day")
    calendar_month_id = fields.Many2one('calendar.month', hidden_field=True)
    employees_ids = fields.Many2many('hr.employee')


# class working_schedule_shifts(models.Model):
#     _name = 'working_schedule_shifts.working_schedule_shifts'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100