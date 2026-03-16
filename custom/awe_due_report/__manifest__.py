# -*- coding: utf-8 -*-
{
    'name': "awe_custmize_date",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        change the datetime to date in order date and commitment date and request date
        / showing total cost field in the list view
    """,

    'author': "Digizilla",
    'website': "http://www.digizilla.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account_followup'],

    # always loaded
    'data': [
        'views/views.xml'

    ],

}