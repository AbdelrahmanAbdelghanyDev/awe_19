# -*- coding: utf-8 -*-
{
    'name': "custom_opportunity_cost_estimation_v11",

    'summary': """
         Adding Cost estimation to the sales module.
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Digizilla_M.Rizk",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '19.0.1.0.0',
    'installable': True,
    'application': False,

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'web',
        'crm',
        'sale_management',
        'product',
        'project',
        'hr_timesheet',
        'stock',
        'account_accountant',
        'account',
        'uom',
        'sector'
    ],


    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'data/data.xml',
        'views/cost_estimate_views.xml',
        'views/project.xml',
        'views/sales.xml',
        'views/task.xml',
        # 'views/templates.xml',
        # 'views/estimation_template_changes_view.xml',
        'views/quotation_estimation_inherit.xml',
        'views/budget_unit_invisible_inherit.xml',
        'views/teams.xml',
        'security/user_groups.xml',
        'views/invoice_form_inherit.xml'
        # 'security/ir.model.access.csv',
    ],


    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
        'assets': {
            'web.assets_backend': [
                'custom_opportunity_cost_estimation_v11/static/src/js/widget.js',
            ],
            'web.assets_qweb': [
                'custom_opportunity_cost_estimation_v11/static/src/xml/**/*',
            ],
        },

}
