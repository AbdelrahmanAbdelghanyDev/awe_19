# -*- coding: utf-8 -*-
{
    'name': "multicurrency_revaluation",

    'summary': """Manage revaluation for multicurrency environment""",

    'author': "Digizilla",
    'website': "http://www.digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant','journal_entry_currency'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/res_conf.xml',
        'views/templates.xml',
        'security/security.xml',
        'views/wizard_currency_revaluation_view.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
