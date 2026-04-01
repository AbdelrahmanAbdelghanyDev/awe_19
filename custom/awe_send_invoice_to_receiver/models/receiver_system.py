# -*- coding: utf-8 -*-

from odoo import models, fields, api

class receiver_system(models.Model):
    _name = 'receiver.system'

    server_url = fields.Char('Server Url')
    db_name = fields.Char('DB Name')
    db_user = fields.Char('DB User')
    db_password = fields.Char('DB Password')
    syncronize = fields.Boolean('Syncronize')

