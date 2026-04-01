# -*- coding: utf-8 -*-
{
    'name': "CancelInvoicePaid",

    'summary': """
        Make Cancel Invoice button visible in draft, open, and paid state""",

    'description': """
        Make Cancel Invoice button visible in draft, open, and paid state
    """,

    'author': "Digizilla",
    'website': "http://www.Digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}