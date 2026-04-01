from odoo import api, fields, models, _
from odoo.http import request



class HrLeave(models.Model):
    _inherit = 'hr.leave'


    employee_manager = fields.Many2one('res.users', related='employee_id.parent_id.user_id', store=True)
    second_approved = fields.Boolean(
        string='',
        required=False)
    manager_approved = fields.Boolean(
        string='',
        required=False)


    def manager_approve(self):
        self.write({'state': 'validate1'})
        approver_users = self.env['res.users'].has_group('awe_leaves_approve.leave_approve_group')
        print('approver_users >>', approver_users)
        if approver_users:
            for employee in self.employee_ids:
                for user in approver_users:
                    print('user', user)
                    notification_ids = [(0, 0, {
                        'res_partner_id': user.partner_id.id,
                        'notification_type': 'inbox'})]
                    self.message_post(record_name='Leave Request',
                                     body=""" Leave Request from employee has been Created: """ + employee.name + """
                                                                                                                        <br> You can access details from here: <br>"""
                                          + """<a href=%s>Link</a>""" % (
                                              self.leave_request_page(self.id))
                                     , message_type="notification",
                                     subtype_xmlid="mail.mt_comment",
                                     author_id=self.env.user.partner_id.id,
                                     notification_ids=notification_ids)

    def final_approve(self):
        self.write({'state': 'validate'})
        self.second_approved = True

    def leave_request_page(self, leave_request):
        menu_id = self.env.ref('hr_holidays.menu_open_department_leave_approve')
        action_id = self.env.ref('hr_holidays.hr_leave_action_action_approve_department')
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (leave_request, 'hr.leave')
        base_url += '&menu_id=%d&action=%s' % (menu_id.id, action_id.id)
        print('base_url', base_url)
        return base_url

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.employee_ids:
            for employee in res.employee_ids:
                if employee.parent_id:
                    notification_ids = [(0, 0, {
                        'res_partner_id': employee.parent_id.user_id.partner_id.id,
                        'notification_type': 'inbox'})]
                    res.message_post(record_name='Leave Request',
                                     body=""" Leave Request from employee has been Created: """ + employee.name + """
                                                                                                    <br> You can access details from here: <br>"""
                                          + """<a href=%s>Link</a>""" % (
                                              res.leave_request_page(res.id))
                                     , message_type="notification",
                                     subtype_xmlid="mail.mt_comment",
                                     author_id=res.env.user.partner_id.id,
                                     notification_ids=notification_ids)
                    print('manager notified')
        return res