# -*- coding: utf-8 -*-
{
    'name': "fleet-rental",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Ahmed Elkfafy",
    'website': "https://www.github.com/elkfafy",

    'category': 'fleet',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'fleet'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/car_rental.xml',
    ],
    'installable': True,
    'application': False,
    'liscense': 'LGPL-3'
}

