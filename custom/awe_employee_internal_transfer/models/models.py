from odoo import api, fields, models



class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    internal_transfer_ids = fields.One2many(
       comodel_name='internal.transfer',
       inverse_name='employee_id',
       string='Internal Transfer',
       required=False)



class InternalTransfer(models.Model):
    _name = 'internal.transfer'

    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        required=False)
    last_department_id = fields.Many2one('hr.department', string='Last Department')
    current_department_id = fields.Many2one('hr.department', string='Current Department')
    date = fields.Date(
        string='Date',
        required=False)
