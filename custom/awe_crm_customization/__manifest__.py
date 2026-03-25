# -*- coding: utf-8 -*-
{
    'name': "AWE Crm Customization",
    'depends': ['base', 'crm', 'cost_estimation'],

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