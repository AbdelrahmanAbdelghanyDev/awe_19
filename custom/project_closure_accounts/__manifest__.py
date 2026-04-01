# -*- coding: utf-8 -*-
{
    'name': "ProjectClosureAccounts",

    'summary': """
        Customization for Account and Project modules""",

    'description': """
        Cost Recog button that creates journal entries for completed projects,
        And Revenue Recog creates journal entry for revenue.
    
    """,

    'author': "Digizilla",
    'website': "http://www.Digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account_accountant', 'custom_project', 'sale_timesheet'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/custom_project_task_view.xml',
        'views/project_closure_accounts_views.xml',
        'views/custom_account_move_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}