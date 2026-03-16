# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, RedirectWarning



# class addition_deduction_segmatek(models.Model):
#     _name = 'addition.deduction'
#
#     name = fields.Char()
#     description = fields.Char()
#     my_type = fields.Selection([('a', 'Amount'), ('d', 'Days')])
#     my_cat = fields.Selection([('a', 'Addition'), ('d', 'Deduction')])
#     default_value = fields.Float()
#     chk = fields.Boolean()
#     first_approval = fields.Many2one('res.users')
#     second_approval = fields.Many2one('res.users')
#     third_approval = fields.Many2one('res.users')
#     configs_id = fields.Many2one('res.config.mysetting')


class ResConfigSetting(models.Model):
    _name = 'res.config.mysetting'

    # _rec_name = 'addition_ded_ids'
    # name = fields.Char()
    name = fields.Char()
    description = fields.Char()
    my_type = fields.Selection([('a', 'Amount'), ('d', 'Days')])
    my_cat = fields.Selection([('a', 'Addition'), ('d', 'Deduction')])
    default_value = fields.Float()
    chk = fields.Boolean(string="Value can't be changed")
    first_approval = fields.Many2one('res.users')
    second_approval = fields.Many2one('res.users')
    third_approval = fields.Many2one('res.users')
    salary_rule_done = fields.Boolean(default=False)
    code = fields.Char()
    # addition_ded_ids = fields.One2many('addition.deduction', 'configs_id')
    IncludeTax = fields.Boolean(string='Company Tax')

    @api.model
    def get_values(self):
        res = super(ResConfigSetting, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()

        addition_ded_ids = ICPSudo.get_param(
            'addition_deduction_segmatek.addition_ded_ids')

        res.update(
            addition_ded_ids=int(addition_ded_ids),
        )
        return res


    def set_values(self):
        super(ResConfigSetting, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param(
            'addition_deduction_segmatek.addition_ded_ids', self.addition_ded_ids)


class main_add_ded_modle(models.Model):
    _name = 'main.add.deduction'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin', 'format.address.mixin']

    _rec_name= 'employee'


    chek_vala = fields.Boolean(related ='addition.chk' ,default = False)
    chek_vald = fields.Boolean(related ='deduction.chk' ,default=False)
    employee = fields.Many2one('hr.employee')
    date = fields.Datetime()
    conf_id = fields.Many2one('res.config.mysetting')
    type = fields.Selection([('a', 'Addition'), ('d', 'Deduction')])
    addition = fields.Many2one('res.config.mysetting', domain="[('my_cat','!=', 'd')]" ,groups='addition_deduction_segmatek.group_user')
    deduction = fields.Many2one('res.config.mysetting',domain="[('my_cat','!=', 'a')]" ,groups='addition_deduction_segmatek.group_user')
    amount = fields.Float()
    notes = fields.Text()
    state = fields.Selection([('draft', 'Draft'),('w','waiting approval'), ('first', 'First Approval'), ('secapp', 'Second Approval'),
                              ('third', 'third Approval'),
                              ('done', 'Done')
                              ], string='Status',default='draft')

    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user)
    Recurring = fields.Boolean()
    date_from = fields.Datetime()
    date_to = fields.Datetime()


    def open_recrurring_model(self):
        self.ensure_one()
        domain = [
            ('employee', '=', self.employee.id),('Recurring', '=', True)]
        return {
            'name': 'Addition & Deduction',
            'domain': domain,
            'res_model': 'main.add.deduction',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'limit': 80,
            'context': "{'default_employee': '%s'}" % self.employee.id
        }


    @api.onchange('addition')
    #
    def cal_amount(self):
        self.amount = self.addition.default_value
        # self.chek_val = self.addition.default_value
        # print (self.chek_val,'AAAAAAAAAAAAAAAAAAAAAZZZZZZZZZZ')

    @api.onchange('deduction')
    def cal_amount_d(self):
        # for rec in self:
        self.amount = self.deduction.default_value
        # print(rec.amount)

    # @api.model
    # def create(self, vals):
    #     cofig_setting_add = self.env['res.config.mysetting'].search(
    #         [('id', '=', vals['addition'])])
    #
    #     cofig_setting_ded = self.env['res.config.mysetting'].search(
    #         [('id', '=', vals['deduction'])])
    #     print(cofig_setting_add.default_value,'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    #     if ['addition']:
    #         # vals['amount']
    #         vals['amount'] = cofig_setting_add.default_value
    #         print (vals['amount'],'bbbbbbbbbbbbbbbbbbb')
    #     if ['deduction']:
    #         vals['amount'] = cofig_setting_ded.default_value
    #     print('valssssssss beforeee supeeeeeer', vals)
    #     return super(main_add_ded_modle, self).create(vals)

    #
    # @api.depends('addition','deduction')
    # def comp_amount(self):
    #     for rec in self:
    #         checked = False
    #         if rec.addition:
    #             rec.amount = rec.addition.default_value
    #             checked = rec.addition.chk
    #         elif rec.deduction:
    #             rec.amount = rec.deduction.default_value
    #             checked = rec.deduction.chk
    #         domain = {'amount': checked}
    #         return {'readonly': domain}


    def set_first(self):
        for rec in self:
            if self.env.user.id == rec.addition.first_approval.id or self.env.user.id == rec.deduction.first_approval.id or self.env.user.id == rec.addition.second_approval.id or self.env.user.id == rec.deduction.second_approval.id or self.env.user.id == rec.addition.third_approval.id or self.env.user.id == rec.deduction.third_approval.id or self.env.user.has_group('addition_deduction_segmatek.group_Manager'):
                return self.write({
                    'state': 'first',
                })
            else:
                raise ValidationError(
                    "this user can't approve please connect your admin")


    def set_wait(self):
        return self.write({
            'state': 'w',
        })


    def set_sec(self):
        for rec in self:
            if self.env.user.id == rec.addition.second_approval.id or self.env.user.id == rec.deduction.second_approval.id or self.env.user.id == rec.addition.third_approval.id or self.env.user.id == rec.deduction.third_approval.id or self.env.user.has_group('addition_deduction_segmatek.group_Manager'):
                return self.write({
                    'state': 'secapp',
                })
            else:
                raise ValidationError(
                    "this user can't approve please connect your admin")


    def set_third(self):
        for rec in self:
            if self.env.user.id == rec.addition.third_approval.id or self.env.user.id == rec.deduction.third_approval.id or self.env.user.has_group('addition_deduction_segmatek.group_Manager'):
                return self.write({
                    'state': 'third',
                })
            else:
                raise ValidationError(
                    "this user can't approve please connect your admin")


    def set_done(self):
        return self.write({
            'state': 'done',
        })
