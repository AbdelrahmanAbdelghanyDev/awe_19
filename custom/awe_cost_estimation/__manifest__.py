# -*- coding: utf-8 -*-
{
    'name': "awe_cost_estimation",

    'summary': """
        This is a specific customization for custom_opportunity_cost_estimation for AWE
        company.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Digizilla",
    'website': "http://www.digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'custom_opportunity_cost_estimation_v11','product','hr','crm'],

    # always loaded
    'data': [
        'data/data.xml',
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/crm_methodolgy_view_inhert.xml',
        'views/budget_view_inherit.xml',
        'views/product_category_inherit.xml'
        # 'reports/report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}