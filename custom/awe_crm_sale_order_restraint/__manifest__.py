# -*- coding: utf-8 -*-
{
    'name': "Crm Drag And state",

    'summary': """
    module to drag and drop state and change state in form
       """,

    'author': "Centione",
    'website': "http://www.centione.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm'],

    # always loaded
    'data': [
        'security/groups.xml',
        'views/crm_stage.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
