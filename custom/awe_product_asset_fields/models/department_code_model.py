from odoo import fields, models, api


class DepartmentCode(models.Model):
    _name = 'department.code.model'
    _description = 'Department Code Model'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
