# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class HRHoliday(models.Model):
    _inherit = 'hr.leave'

    def _validate_leave_request(self):
        for rec in self:
            rec.holiday_status_id.create_calendar_meeting = False
        super(HRHoliday, self)._validate_leave_request()
