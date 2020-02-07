# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Vendor Onboarding",
    'author': 'Ascetic Business Solution',
    'category': 'sale',
    'summary': """Vendor Onboarding""",
    'license': 'OEEL-1',
    'website': 'http://www.asceticbs.com',
    'description': """Vendor Onboarding""",
    'version': '1.0',
    'depends': ['bi_customer_supplier_approve','website'],
    'data': [
             'view/onboarding_template.xml',
             'view/res_partner_view.xml',
             'data/website_portal_tmpl_view.xml',
            ],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
