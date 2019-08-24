# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Move Product Price',
    'category': 'Hidden',
    'version': '1.0',
    'description':
        """
Using the Web modules the price will be moved.
========================

This module will move the Product price on the product page above the attributes and place under the Product Name.
        """,
    'depends': ['website_sale'],
    'auto_install': False,
    'data': [
        'views/assets.xml',
        'views/templates.xml',
    ]
}
