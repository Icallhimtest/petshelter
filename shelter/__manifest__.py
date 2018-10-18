# -*- coding: utf-8 -*-
{
    'name': "shelter",

    'summary': """
        Shelter app, appointments, patients.""",

    'description': """
        This app provides the features needed by any shelter.
    """,

    'author': "Denis Ledoux",
    'website': "http://www.ldx.be",
    'category': 'Shelter',
    'version': '0.1',
    'depends': ['base', 'mail'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/common.xml',
        'views/animal.xml',
        'views/patient.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
