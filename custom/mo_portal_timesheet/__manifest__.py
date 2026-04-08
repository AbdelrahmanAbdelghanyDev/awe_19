# -*- coding: utf-8 -*-
{
    'name': "MO Portal Timesheet",
    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '19.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'portal', 'hr_timesheet', 'web', 'website'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # 'mo_portal_timesheet/static/js/choosen.js',
            'mo_portal_timesheet/static/css/select2.min.css',
            'mo_portal_timesheet/static/js/select2.min.js',
        ],
        'web.assets_frontend_lazy': [
            'mo_portal_timesheet/static/js/portal_timesheet.js',
        ],
    },
}
