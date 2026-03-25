from odoo import models, fields, api, _


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    employee_id = fields.Many2one('hr.employee')


class HrDocumentType(models.Model):
    _name = 'hr.document.type'

    name = fields.Char(required=True)

    attachment_ids = fields.Many2many('ir.attachment')

    def sync_attachment(self):
        for rec in self:
            for attach in rec.attachment_ids:
                if not attach.employee_id:
                    name = attach.name
                    employee_code = name.split('_')
                    employee = self.env['hr.employee'].search([('code', '=', employee_code)], limit=1)
                    if employee:
                        found_type = False
                        for line in employee.document_ids:
                            if line.type_id.id == rec.id:
                                found_type = True
                                line.documents_ids = [(0, 0, {'document': attach.datas, 'name': attach.name})]
                        if not found_type:
                            employee.document_ids = [(0, 0, {'type_id': rec.id, 'documents_ids': [
                                (0, 0, {'document': attach.datas, 'name': attach.name})]})]
                        attach.employee_id = employee.id
