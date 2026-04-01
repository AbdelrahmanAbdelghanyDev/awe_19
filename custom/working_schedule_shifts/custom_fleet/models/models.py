# -*- coding: utf-8 -*-

from odoo import models, fields, api

class custom_fleet(models.Model):
    _inherit = 'fleet.vehicle'

    vehicleID = fields.Char('Vehicle ID')
    department = fields.Many2one('custom_fleet.department', string='Department')
    purchaseDate = fields.Date('Purchase Date')
    motorNumber = fields.Char('Motor Number')
    costCenter = fields.Char('Cost Center')
    licenseType = fields.Many2one('custom_fleet.license_type', string='License Type')
    notes = fields.Text('Notes')

class license_type(models.Model):
    _name = 'custom_fleet.license_type'

    name = fields.Char('License Type')

class department(models.Model):
    _name = 'custom_fleet.department'

    name = fields.Char('Department Name')

