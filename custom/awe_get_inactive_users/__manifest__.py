# -*- coding: utf-8 -*-
{
    'name': "AWE Get Inactive Users",
    'depends': ['base', 'sale', 'crm'],

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