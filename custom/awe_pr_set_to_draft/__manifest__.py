# -*- coding: utf-8 -*-
{
    'name': "awe pr set to draft",

    'summary': """
      button draft applied on sepcifc group to reset to draft sale order
      """,

    'author': "Centione",
    'website': "http://www.centione.com",


    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'security/groups.xml',
    ],
    # only loaded in demonstration mode
}