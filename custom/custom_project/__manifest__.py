# -*- coding: utf-8 -*-
{
    'name': "CustomProject",

    'summary': """
        Customization for  Project Module Reports """,

    'description': """
        Customization for  Project Module Reports
    """,

    'author': "Digizilla",
    'website': "http://www.digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'hr_timesheet','awe_cost_estimation', 'custom_opportunity_cost_estimation_v11','crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
        'reports.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {

        'web.report_assets_common': [
            '/custom_project/static/src/css/style.css',
        ],
    },

}
