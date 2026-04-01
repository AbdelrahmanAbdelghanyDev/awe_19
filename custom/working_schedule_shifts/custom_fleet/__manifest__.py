# -*- coding: utf-8 -*-
{
    'name': "CustomFleet",

    'summary': """
        A customized Fleet Management Module""",

    'description': """
        The following fields were added to the fleet management module:
       vehicleID, department, purchaseDate, motorNumber, costCenter, licenseType, and notes.
    """,

    'author': "Digizilla",
    'website': "http://www.digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'fleet'],

    # always loaded
    'data': [
        'views/custom_fleet_views.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}