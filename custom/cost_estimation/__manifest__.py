{
    'name': "Cost Estimation",

    'summary': """
    General Cost Estimation Module""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Digizilla",
    'website': "http://www.digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'crm',
    'version': '11',

    # any module necessary for this one to work correctly
    'depends': ['base','awe_cost_estimation','account','new_awe_edits','custom_opportunity_cost_estimation_v11','account_budget','uom'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        # 'views/settings.xml',
        'views/crm.xml',
        'views/cost_estimation.xml',
        'views/product.xml',
        'views/quotation.xml',
        'views/templates.xml',
        'views/account_budget.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
# -*- coding: utf-8 -*-
