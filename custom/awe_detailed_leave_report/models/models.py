# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import fields, models, api, _
from odoo.exceptions import UserError
import xlsxwriter
from io import BytesIO
import base64
from datetime import datetime, time, date
from odoo.exceptions import ValidationError
import base64
import os
import logging
# try:
#     from urllib2 import urlopen
# except ImportError:
#     from urllib.request import urlopen
from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError
from odoo import models, fields, api


class DetailedLeaveWizard(models.TransientModel):
    _name = 'detailed.leave.excel'

    excel_file = fields.Binary('Download report Excel', attachment=True, readonly=True)
    file_name = fields.Char('Excel File', size=64)
    employee_ids = fields.Many2many('hr.employee', required=True)
    leave_type = fields.Many2many('hr.leave.type', required=True)

    def action_leave_report(self):
        leave_types = []
        self = self.sudo()
        employees = self.employee_ids
        for type in self.leave_type:
            data = []
            for rec in employees:
                request = 0
                allocation = 0
                records = rec.env['hr.leave'].search(
                    [('employee_id', '=', rec.id),
                     ('holiday_status_id', '=', type.id), ('state', '=', 'validate')])
                request += sum([item.number_of_days for item in records])
                records = rec.env['hr.leave.allocation'].search(
                    [('employee_id', '=', rec.id),
                     ('holiday_status_id', '=', type.id), ('state', '=', 'validate')])
                allocation += sum([item.number_of_days for item in records])

                data.append(
                    [rec.name, type.name, round(allocation, 2), round(request, 2),
                     round(allocation - request, 2)])
            leave_types.append(data) if data else print('d')
        if leave_types:
            act = self.generate_excel(leave_types)
            return act
        else:
            raise ValidationError(_('No Records To Show'))

    def generate_excel(self, leave_types):

        filename = 'Detailed Leave Report'
        # % (data[0][2]))
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet(filename)
        for data in leave_types:

            without_borders = workbook.add_format({
                'bold': 1,
                'border': 0,
                'align': 'center',
                'valign': 'vcenter',
                'text_wrap': True,
                'font_size': '11',

            })

            font_size_10 = workbook.add_format(
                {'font_name': 'KacstBook', 'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
                 'border': 1})
            font_size_12 = workbook.add_format(
                {'font_name': 'KacstBook', 'font_size': 13, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
                 'border': 1})
            font_size_green = workbook.add_format(
                {'font_name': 'KacstBook', 'bg_color': '#008000', 'font_size': 10, 'align': 'center',
                 'valign': 'vcenter',
                 'text_wrap': True,
                 'border': 1})

            table_header_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'bg_color': '#AAB7B8',
                'font_size': '10',
                'align': 'center',
                'valign': 'vcenter',
                'text_wrap': True
            })
            sheet.set_column(0, 0, 5)
            sheet.set_column(1, 1, 35)
            sheet.set_column(2, 15, 20)
            row = 1
            col = -1
            no = 0
            sheet.write(row, col + 1, "NO", table_header_format)
            sheet.write(row, col + 2, "Name", table_header_format)
            sheet.write(row, col + 3, "Leave Type", table_header_format)
            sheet.write(row, col + 4, "Allocation", table_header_format)
            sheet.write(row, col + 5, "Request", table_header_format)
            sheet.write(row, col + 6, "Remaining", table_header_format)
            for rec in data:
                row += 1
                sheet.write(row, col + 1, str(no + 1), font_size_10)
                sheet.write(row, col + 2, str(rec[0]), font_size_10)
                sheet.write(row, col + 3, str(rec[1]), font_size_10)
                sheet.write(row, col + 4, str(rec[2]), font_size_10)
                sheet.write(row, col + 5, str(rec[3]), font_size_10)
                sheet.write(row, col + 6, str(rec[4]), font_size_10)
                no += 1

        workbook.close()
        output.seek(0)

        self.write({'file_name': 'Detailed Leave Report' + str(datetime.today().strftime('%Y-%m-%d')) + '.xlsx'})
        self.excel_file = base64.b64encode(output.read())

        return {
            'type': 'ir.actions.act_url',
            'name': 'Detailed Leave Report',
            'url': '/web/content/detailed.leave.excel/%s/excel_file/%s.xlsx?download=true' % (
                self.id, 'Detailed Leave Report'),
            'target': 'new'
        }
