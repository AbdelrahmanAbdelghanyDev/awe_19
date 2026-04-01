# -*- coding: utf-8 -*-
{
    'name': "awe_hide_link",

    'author': "Centione",
    'website': "http://www.centione.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm','cost_estimation'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        # 'views/templates.xml',
    ]
}
