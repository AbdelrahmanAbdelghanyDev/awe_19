# -*- coding: utf-8 -*-
{
    'name': "AWE Budget and Forecast",

    'summary': """
        this is an app to create a report from clients based on quarters and compare between them""",

    'description': """
        this is an app to create a report from clients based on quarters and compare between them
    """,

    'author': "Abdelrahman ShamrouKh/Abdullah Nassar || Centione",
    'website': "http://www.centione.com",
    'category': 'business',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'sector', 'sales_team', 'awe_cost_estimation'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
