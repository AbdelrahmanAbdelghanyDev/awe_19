# -*- coding: utf-8 -*-
{
    'name': "change_currency_rate_format",

    'summary': """
        Change currency rate format to be for example  ( USD to EGP 20 ) instead of (1/20) by adding a field to enter the normal rate 20 and convert the original odoo field to a computed field""",

    'description': """
        Change currency rate format
    """,

    'author': "Digizilla",
    'website': "http://www.digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/res_currency_rate_inherit.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}