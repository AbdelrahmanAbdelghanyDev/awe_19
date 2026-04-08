# -*- coding: utf-8 -*-
{
    'name': "Invoice QR Report",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Accounting Report',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account','awe_official_name'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views_3.xml',
        # 'views/views.xml',
        # 'views/nakham2.xml',
        'views/templates.xml',
    ]
}
