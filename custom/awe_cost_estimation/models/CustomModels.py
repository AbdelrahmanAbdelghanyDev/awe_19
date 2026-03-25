# -*- coding: utf-8 -*-

from odoo import models, fields, api

SEC = [
    ('A', 'A'),
    ('AB', 'AB'),
    ('BC1', 'BC1'),
    ('C1', 'C1'),
    ('C2', 'C2'),
    ('C1C2', 'C1C2'),
    ('C2D', 'C2D'),
    ('D', 'D'),
    ('E', 'E'),
    ('DE', 'DE'),
]


class ProjectObjective(models.Model):
    _name = 'project.objective'

    name = fields.Char()


class ResearchType(models.Model):
    _name = 'research.type'

    name = fields.Char(string='Research Type')


class DataCapture(models.Model):
    _name = 'data.capture'

    name = fields.Char(string='Data Capture')
