# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import xlwt
import datetime
import base64
from io import StringIO
from datetime import datetime
from odoo import api, fields, models, _
import platform

class PayslipReportOut(models.Model):
    _name = 'wizard.reports.out'
    _description = 'payslip report'

    payslip_data = fields.Char('Name', size=256)
    file_name = fields.Binary('Payslip Excel Report', readonly=True)
    payslip_work = fields.Char('Name', size=256)
    file_names = fields.Binary('Payslip CSV Report', readonly=True)


class ReportWizards(models.Model):
    _name = 'wizard.reports'
    _description = 'Payslip wizard'

    # payslip order excel report button actions
    def action_payslip_report(self):
        # # XLS report
        custom_value = {}
        label_lists = ['PO', 'POR', 'CLIENTREF', 'BARCODE', 'DEFAULTCODE', 'NAME', 'QTY', 'VENDORPRODUCTCODE', 'TITLE',
                       'PARTNERNAME', 'EMAIL', 'PHONE', 'MOBILE', 'STREET', 'STREET2', 'ZIP', 'CITY', 'COUNTRY']
        payslip = self.env['hr.payslip'].browse(self._context.get('active_ids', list()))
        print('xx',payslip)
        workbook = xlwt.Workbook()
        style0 = xlwt.easyxf(
            'font: name Times New Roman bold True, height 200;borders:left thin, right thin, top thin, bottom thin;align: horiz center;')

        sheet = workbook.add_sheet("Payslip",cell_overwrite_ok=True)
        sheet.write(0, 0, 'Row',style0)
        sheet.write(0, 1, 'Branch',style0)
        sheet.write(0, 2, 'Employee id',style0)
        sheet.write(0, 3, 'Account Number',style0)
        sheet.write(0, 4, 'Name',style0)
        sheet.write(0, 5, 'Code',style0)
        sheet.write(0, 6, 'Reasons',style0)
        sheet.write(0, 7, 'Amount',style0)
        row = 1
        for rec in payslip:
            sheet.write(row, 0, row,style0)
            sheet.write(row, 1, rec.employee_id.branch,style0)
            sheet.write(row, 2, rec.employee_id.bank_id,style0)
            sheet.write(row, 3, rec.employee_id.bank_account_id.acc_number,style0)
            sheet.write(row, 4, rec.employee_id.name,style0)

            sheet.write(row, 6, 'Salaries %s %s'%(datetime.strptime(
                rec.date_from, '%Y-%m-%d').strftime('%B'),datetime.strptime(
                rec.date_from, '%Y-%m-%d').year),style0)
            sheet.write(row, 7, self.env['hr.payslip.line'].search([('slip_id','=',rec.id),
                                                                     ('code','=','NET')]).total,style0)
            row = row+1

        output = StringIO()
        label = (';'.join(label_lists))
        output.write(label)
        output.write("\n")


        data = base64.b64encode(bytes(output.getvalue(), "utf-8"))

        filename = ('/Payslip/Report-' + str(datetime.today().date()) + '.xls')


        # filename = filename.split('/')[2]
        # filename2 = filename2.split('/')[2]
        workbook.save(filename)
        fp = open(filename, "rb")
        file_data = fp.read()
        out = base64.encodestring(file_data)

        # Files actions
        attach_vals = {
            'payslip_data': filename,
            'file_name': out,
            'file_names': data,
        }

        act_id = self.env['wizard.reports.out'].create(attach_vals)
        fp.close()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.reports.out',
            'res_id': act_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'context': self.env.context,
            'target': 'new',
        }
