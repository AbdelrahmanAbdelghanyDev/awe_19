# -*- coding: utf-8 -*-
{
    'name': "Sale Order Custom",

    'author': "Centione",
    'website': "http://www.centione.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order.xml',
    ],
}
