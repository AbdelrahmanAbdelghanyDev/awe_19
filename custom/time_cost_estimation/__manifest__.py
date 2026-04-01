# -*- coding: utf-8 -*-
{
    'name': "Time Cost Estimation",
    'author': "Centione",
    'website': "http://www.yourcompany.com",

    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'account_budget', 'cost_estimation', 'crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
