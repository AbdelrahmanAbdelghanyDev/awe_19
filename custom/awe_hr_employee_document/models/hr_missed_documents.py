# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
from odoo.osv import expression


class HrMissedDocuments(models.Model):
    _name = "hr.missed.documents"
    _description = 'Missed Documents Summary / Report'
    _auto = False
    _order = "employee_id"

    employee_id = fields.Many2one('hr.employee', string="Employee", readonly=True)
    active_employee = fields.Boolean(related='employee_id.active', readonly=True)
    # code = fields.Char(related='employee_id.code', readonly=True)
    name = fields.Char(related='type_id.name', readonly=True)
    type_id = fields.Many2one("hr.document.type", string="Type", readonly=True)
    company_id = fields.Many2one('res.company', string="Company", related='employee_id.company_id', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, 'hr_missed_documents')

        self._cr.execute("""
            CREATE or REPLACE view hr_missed_documents as (
                SELECT row_number() over(ORDER BY records.employee_id) as id,
                records.employee_id as employee_id, records.type_id as type_id
                from (select cross_join.employee_id , cross_join.type_id from (select employee.id as employee_id ,doc_type.id as type_id
                    from hr_employee as employee
                    CROSS JOIN hr_document_type as doc_type) as cross_join
                    where NOT EXISTS (select document.employee_id ,document.type_id from hr_document as document
                     where document.done != False and document.employee_id = cross_join.employee_id and document.type_id = cross_join.type_id )
                    ) records
            );
        """)

