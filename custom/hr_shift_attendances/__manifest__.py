# -*- coding: utf-8 -*-
{
    'name': "HRShiftAttendances",

    'summary': """
        This module handles the attendance of shift based employees.""",

    'description': """
        This module handles the attendance of shift based employees as well as standard working time employees.
    """,

    'author': "DigiZilla",
    'website': "http://www.Digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_attendance', 'resource', 'hr_payroll', 'working_schedule_shifts','mail','contacts','hr'],

    # always loaded
    'data': [
        'data/data.xml',
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/hr_employee_view.xml',
        'views/wizard_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}