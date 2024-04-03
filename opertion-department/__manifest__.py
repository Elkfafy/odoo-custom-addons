# -*- coding: utf-8 -*-
{
    'name': "operation-department",

    'summary': "This is the module for operation department",

    'description': """
    We used this module to bulid the essential base for operation department for monetring and doing there job
    """,

    'author': "Ahmed Elkfafy",
    'website': "https://www.github.com/elkfafy",

    'category': 'fleet',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'fleet', 'fleet_rental'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/operation_page.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}

