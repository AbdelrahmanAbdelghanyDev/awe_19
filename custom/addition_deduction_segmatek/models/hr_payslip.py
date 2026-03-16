from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.translate import _
import time
from datetime import datetime
from datetime import time as datetime_time
from dateutil import relativedelta



class HrPayslipCustom(models.Model):
    _inherit = 'hr.payslip'

    date_from = fields.Date(string='Date From', readonly=True, required=True,
                            default=time.strftime('%Y-%m-20'), states={'draft': [('readonly', False)]})
    date_to = fields.Date(string='Date To', readonly=True, required=True,
                          default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=18))[:10],
                          states={'draft': [('readonly', False)]})



    def calculate_addition(self,payslip):
        payslip_obj = self.search([('id','=', payslip)])
        datej = fields.Datetime.from_string(payslip_obj.date_to)
        datek = fields.Datetime.from_string(payslip_obj.date_from)

        additions = self.env['main.add.deduction'].search([('type', '=', 'a'),
                                                   ('date','>=', str(datek)),#payslip_obj.date_from),
                                                   ('date','<=', str(datej)),#payslip_obj.date_to),
                                                   ('employee','=', payslip_obj.employee_id.id)])
        total = 0
        days = 0
        contract_obj = self.env['hr.contract'].search([('employee_id', '=', payslip_obj.employee_id.id)], limit=1)
        print (contract_obj.dsalary, 'AAAAAAAAAAAAAAa')
        for add in additions:
            if add.addition.my_type == 'a' :
                total += add.amount
                # return total
            elif add.addition.my_type == 'd' :
                days += add.amount

        total += days * contract_obj.dsalary
        return total


    def calculate_deduction(self, payslip):
        payslip_obj = self.search([('id', '=', payslip)])
        datej = fields.Datetime.from_string(payslip_obj.date_to)
        datek = fields.Datetime.from_string(payslip_obj.date_from)
        deductions = self.env['main.add.deduction'].search([('type', '=', 'd'),
                                                           ('date', '>=', str(datek)),  # payslip_obj.date_from),
                                                           ('date', '<=', str(datej)),  # payslip_obj.date_to),
                                                           ('employee', '=', payslip_obj.employee_id.id)])
        total = 0
        days = 0
        contract_obj = self.env['hr.contract'].search([('employee_id', '=', payslip_obj.employee_id.id)], limit=1)
        print (contract_obj.dsalary,'DDDDDDDDDDDD')
        for add in deductions:
            if add.deduction.my_type == 'a':
                total += add.amount

                # return total * -1
            elif add.deduction.my_type == 'd':
                days += add.amount
        total += days * contract_obj.dsalary
        print ('TTTTTTTTTTo',total)

        return total * -1



