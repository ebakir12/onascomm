{
    'name': 'Automate the Pricelist upload',
    'category': 'Website',
    'sequence': 55,
    'summary': 'Provids a model to upload a product and automate the different pricelists',
    'website': '',
    'version': '1.1',
    'description': "Model that enables the Product Attribute to determine what all the items within a pricelist should be.  This only provides support for a single selection.",
    'depends': ['base', 'website', 'sale_payment', 'product', 'sale', 'website_sale_options'],
    'data': [
        'security/ir.model.access.csv',
        'data/action_menu.xml'
    ],
    'installable': True,
}
