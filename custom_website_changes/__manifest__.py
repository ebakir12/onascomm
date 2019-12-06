# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'eCommerce Custom Website Changes',
    'category': 'Website',
    'version': '1.0',
    'website': '',
    'description': """
Odoo E-Commerce
==================
Custom Changes to the website:
-Add custom field to Template to display in Sales Ribbon 

        """,
    'depends': ['website_sale'],
    'data': [
        'views/product_views.xml'
    ],
    'installable': True,
}
