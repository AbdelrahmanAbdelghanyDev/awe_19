{
    'name': "Portal Attendance",

    'summary': """
        Portal user can Check in / Out through Portal""",

    'description': """
        Portal user can Check in / Out through Portal
        User must have related Employee
    """,

    'author': "Digizilla",
    'website': "https://www.digizilla.net",

    'category': 'Hr',
    'version': '19.0.1.0.0',

    'depends': ['base', 'web', 'portal', 'website', 'hr_attendance'],

    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}