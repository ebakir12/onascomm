# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Mobile Savvy',
    'description': 'Website Mobile Savvy',
    'category': 'Theme/Business',
    'version': '11.0.1.0.0',
    'summary': 'Multi Purpose,Responsive and Fully '
               'Customizable Odoo Theme',
    'author': '73Lines',
    'depends': [
        'website',
        'website_crm',
        'carousel_slider_73lines',
        'snippet_product_carousel_73lines',
    ],
    'data': [
        'views/assets.xml',
        'views/login.xml',
        'views/homepage.xml',
        'views/home-personal.xml',
        'views/header.xml',
        #'views/footer_template.xml',
        'views/aboutus_template.xml',
        'views/contactus_template.xml',
        'views/testimonial.xml',
        # Snippets
    ],
    'demo': [
    ],
    'images': [
        'static/description/leo-banner.png',
    ],
    'license': 'OPL-1',
}
