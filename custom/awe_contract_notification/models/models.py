from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.http import request



class Hremployee(models.Model):
    _inherit = 'hr.employee'

    hiring_date = fields.Date(
        string='Hiring Date',
        required=False)

    probation_date = fields.Date(
        string='Probation Date',
        required=False)

    def send_employee_probation_page(self, emp):
        menu_id = self.env.ref('hr.menu_hr_employee_user')
        action_id = self.env.ref('hr.open_view_employee_list_my')
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (emp, 'hr.employee')
        base_url += '&menu_id=%d&action=%s' % (menu_id.id, action_id.id)
        print('base_url', base_url)
        return base_url

    def send_employee_probation_notification(self, partner_id, employee_name, record):
        notification_ids = [(0, 0, {
            'res_partner_id': partner_id,
            'notification_type': 'inbox'
        })]
        self.message_post(record_name='Employee Probation Date Notify',
                          body=""" Probation Date Will Come After 3 Weeks from employee: """ + employee_name + """
           <br> You can access details from here: <br>""" + """<a href=%s>Link</a>""" % (
                              record)
                          , message_type="notification",
                          subtype_xmlid="mail.mt_comment",
                          author_id=self.env.user.partner_id.id,
                          notification_ids=notification_ids)

    def get_probation_notification(self):
        records = self.env['hr.employee'].search([])
        for employee in records:
            if employee.probation_date:
                probation_period = relativedelta(weeks=3)
                diff = employee.probation_date - probation_period
                if diff == fields.Date.context_today(employee):
                    hr_users = self.env['res.users'].search(['|', ('id', '=', 394), ('id', '=', 253)])
                    if hr_users:
                        for record in hr_users:
                            page = employee.send_employee_probation_page(employee.id)
                            employee.send_employee_probation_notification(record.partner_id.id, employee.name, page)


# class HrContract(models.Model):
#     _inherit = 'hr.contract'
#
#     hiring_date = fields.Date(
#         string='Hiring Date',
#         required=False, related='employee_id.hiring_date', store=True)
#
#     def contract_request_page(self, contract_request):
#         menu_id = self.env.ref('hr_contract.hr_menu_contract_history')
#         action_id = self.env.ref('hr_contract.hr_contract_history_view_list_action')
#         base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
#         base_url += '/web#id=%d&view_type=form&model=%s' % (contract_request, 'hr.leave')
#         base_url += '&menu_id=%d&action=%s' % (menu_id.id, action_id.id)
#         print('base_url', base_url)
#         return base_url
#
#     def send_contract_expiration_notification(self, partner_id, employee_name, contract_request_page):
#         notification_ids = [(0, 0, {
#             'res_partner_id': partner_id,
#             'notification_type': 'inbox'
#         })]
#         self.message_post(record_name='Contract Expiration Date Notify',
#                           body=""" Contract Expiration Date Notify from employee: """ + employee_name + """
#          <br> You can access Contract details from here: <br>""" + """<a href=%s>Link</a>""" % (
#                               contract_request_page)
#                           , message_type="notification",
#                           subtype_xmlid="mail.mt_comment",
#                           author_id=self.env.user.partner_id.id,
#                           notification_ids=notification_ids)
#
#     def notify_scheduled(self):
#         records = self.env['hr.contract'].search([])
#         for m in records:
#             if m.date_end:
#                 hr_notify_months = relativedelta(days=135)
#                 manager_notify_month = relativedelta(months=4)
#                 diff_for_hr = m.date_end - hr_notify_months
#                 diff_for_managers = m.date_end - manager_notify_month
#                 if diff_for_hr == fields.Date.context_today(m):
#                     hr_users = self.env['res.users'].search(['|', ('id', '=', 394), ('id', '=', 253)])
#                     if hr_users:
#                         for record in hr_users:
#                             page = m.contract_request_page(m.id)
#                             m.send_contract_expiration_notification(record.partner_id.id, m.employee_id.name,page)
#                 if diff_for_managers == fields.Date.context_today(m):
#                     page = m.contract_request_page(m.id)
#                     m.send_contract_expiration_notification(m.employee_id.parent_id.user_id.partner_id.id, m.employee_id.name,page)