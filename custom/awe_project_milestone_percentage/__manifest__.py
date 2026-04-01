# -*- coding: utf-8 -*-
{
    'name': "AWE Project Milestone Percentage",
    'author': "Centione",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'sale', 'project_closure_accounts',
                'awe_cost_estimation', 'custom_opportunity_cost_estimation_v11'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/project_milestone_setting.xml',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
