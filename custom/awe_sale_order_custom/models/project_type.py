from odoo import api, fields, models 

class ProjectType(models.Model):
    _name = 'res.project.type'
    _description = 'ProjectType'

    name = fields.Char(required=True)
    
