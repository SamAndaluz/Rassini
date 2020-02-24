# -*- coding: utf-8 -*-
{
    'name': "Project portal extended",

    'summary': """
        This module add some fields and functionality to project tasks in web portal.""",

    'description': """
        This module add some fields and functionality to project tasks in web portal.
    """,

    'author': "A. Márquez",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project','website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/project_portal_templates.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
