# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ops_no_create_fields(models.Model):
#     _name = 'ops_no_create_fields.ops_no_create_fields'
#     _description = 'ops_no_create_fields.ops_no_create_fields'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
