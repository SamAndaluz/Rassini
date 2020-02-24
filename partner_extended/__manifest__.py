# -*- coding: utf-8 -*-
{
    'name': "Partner extended",

    'summary': """
        This module add some fields to know if partner is customer or vendor.""",

    'description': """
        This module add some fields to know if partner is customer or vendor.
    """,

    'author': "AMB",
    'website': "",
    
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts','sale','purchase'],

    # always loaded
    'data': [
        'security/partner_security.xml',
        'views/res_partner.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
