# -*- coding: utf-8 -*-
{
    'name': "WorkingScheduleShifts",

    'summary': """
        Module customizing working time resource setting.""",

    'description': """
        This module adds Month Schedules of the year to the working time resource setting.
    """,

    'author': "Digizilla",
    'website': "http://www.Digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_timesheet'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/resources_custom_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}