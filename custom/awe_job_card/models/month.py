# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Month(models.Model):
    _name = 'res.month'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    num = fields.Integer(string='Number', compute='compute_num', store=True)

    @api.depends('name')
    def compute_num(self):
        for rec in self:
            rec.num = False
            if rec.name in ['January', 'january', 'يناير']:
                rec.num = 1
            if rec.name in ['February', 'february', 'فبراير']:
                rec.num = 2
            if rec.name in ['March', 'march', 'مارس']:
                rec.num = 3
            if rec.name in ['April', 'april', 'أبريل', 'ابريل']:
                rec.num = 4
            if rec.name in ['May', 'may', 'مايو']:
                rec.num = 5
            if rec.name in ['June', 'june', 'يونيو']:
                rec.num = 6
            if rec.name in ['July', 'july', 'يوليو']:
                rec.num = 7
            if rec.name in ['August', 'august', 'أغسطس', 'اغسطس']:
                rec.num = 8
            if rec.name in ['September', 'september', 'سبتمبر']:
                rec.num = 9
            if rec.name in ['October', 'october', 'أكتوبر', 'اكتوبر']:
                rec.num = 10
            if rec.name in ['November', 'november', 'نوفمبر']:
                rec.num = 11
            if rec.name in ['December', 'december', 'ديسمبر']:
                rec.num = 12
