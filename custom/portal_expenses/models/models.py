# # -*- coding: utf-8 -*-
# from odoo import models, fields, api, _
# from odoo.exceptions import ValidationError
# from odoo.exceptions import UserError
#
#
# class NotifyMessage(models.Model):
#     _inherit = 'mail.message'
#
#     def notify_user_expen(self, user):
#         try:
#             user = self.env["hr.employee"].browse(user)
#         except Exception as e:
#             pass
#
#         approval_id = self.env['ir.config_parameter'].sudo().get_param('Approval_id')
#         approval_user = self.env["res.users"].browse(int(approval_id))
#
#         # template_obj = self.env['mail.template'].sudo().search([('name', '=', 'Attendance Notification')],limit=1)
#         # body = template_obj.body_html
#
#         body = "ok"
#         mail_values = {
#             'subject': "Expenses notification",
#             'body_html': body,
#             'email_to': approval_user.email,
#             'email_from': user.work_email  # template_obj.email_from,
#         }
#         self.env['mail.mail'].create(mail_values).send()
#
#
# class portal_expenses_inherit(models.Model):
#     _name='portal_expenses'
#     # _inherit = 'portal'
#
#
#     def submit_expenses(self):
#         obj = self.env['mail.message'].search([])[0]
#         obj.notify_user_expen(self.employee_id.id)
#
#
