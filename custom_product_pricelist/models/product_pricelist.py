# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class ProdPricelist(models.Model):
    _name = "product.prices"
    _description = "Used to organize the Pricelists and the Attribute Value to use to compare the prices"

    name = fields.Char(string='Name', required=True)
    bib_attribute_id = fields.Many2one('product.attribute.value', string='Bring it Back')
    attribute1_id = fields.Many2one('product.attribute.value', string='Attribute 1')
    attribute2_id = fields.Many2one('product.attribute.value', string='Attribute 2')
    attribute3_id = fields.Many2one('product.attribute.value', string='Attribute 3')
    attribute4_id = fields.Many2one('product.attribute.value', string='Attribute 4')
    attribute5_id = fields.Many2one('product.attribute.value', string='Attribute 5')
    attribute6_id = fields.Many2one('product.attribute.value', string='Attribute 6')
    pricelist_id = fields.Many2many('product.pricelist', string='Pricelist')
    item_ids = fields.One2many('product.prices.item', 'prices_id', string='Product Items')

class ProdPricelistItems(models.Model):
    _name = "product.prices.item"
    _description = "Pricelist Items that identifies the different prices"

    name = fields.Char(string='Product Name', required=True)
    prices_id = fields.Many2one('product.prices', 'Product Prices', index=True, ondelete='cascade', required=True)
    product_id = fields.Many2one('product.template', 'Product')
    retail_price = fields.Float('Retail Price', default=0, digits=(16, 2))
    bib_price_discount = fields.Float('Bring it Back Discount', default=0, digits=(16, 2))
    attribute1_price = fields.Float('Attribute 1 Price', default=0, digits=(16, 2))
    attribute2_price = fields.Float('Attribute 2 Price', default=0, digits=(16, 2))
    attribute3_price = fields.Float('Attribute 3 Price', default=0, digits=(16, 2))
    attribute4_price = fields.Float('Attribute 4 Price', default=0, digits=(16, 2))
    attribute5_price = fields.Float('Attribute 5 Price', default=0, digits=(16, 2))
    attribute6_price = fields.Float('Attribute 6 Price', default=0, digits=(16, 2))
    hardware_discount = fields.Float('Hardware Discount', default=0, digits=(16, 2))
    taxable_amount = fields.Float('Taxable Amount', default=0, digits=(16, 2))
    att1_price_1 = fields.Float('Attribute 1 Cost /mo', default=0, digits=(16, 2))
    att1_price_2 = fields.Float('Attribute 1 Custom Price 2', default=0, digits=(16, 2))
    att2_price_1 = fields.Float('Attribute 2 Cost /mo', default=0, digits=(16, 2))
    att2_price_2 = fields.Float('Attribute 2 Custom Price 2', default=0, digits=(16, 2))
    att3_price_1 = fields.Float('Attribute 3 Cost /mo', default=0, digits=(16, 2))
    att3_price_2 = fields.Float('Attribute 3 Custom Price 2', default=0, digits=(16, 2))
    att4_price_1 = fields.Float('Attribute 4 Cost /mo', default=0, digits=(16, 2))
    att4_price_2 = fields.Float('Attribute 4 Custom Price 2', default=0, digits=(16, 2))
    att5_price_1 = fields.Float('Attribute 5 Cost /mo', default=0, digits=(16, 2))
    att5_price_2 = fields.Float('Attribute 5 Custom Price 2', default=0, digits=(16, 2))
    att6_price_1 = fields.Float('Attribute 6 Cost /mo', default=0, digits=(16, 2))
    att6_price_2 = fields.Float('Attribute 6 Custom Price 2', default=0, digits=(16, 2))
    product_skus = fields.Char("Product Sku's")

    @api.model
    def create(self, vals):
        # Do some creating here
        product_id = vals['product_id'] if 'product_id' in vals else self.product_id.id
        product_skus = vals['product_skus'] if 'product_skus' in vals else self.product_skus
        vals['product_id'] = self._check_and_set_product(product_id, product_skus)
        
        res = super(ProdPricelistItems, self).create(vals)
        
        res._add_update_pricelist_items()
        
        return res

    @api.multi
    def write(self, vals):
        product_id = vals['product_id'] if 'product_id' in vals else self.product_id.id
        product_skus = vals['product_skus'] if 'product_skus' in vals else self.product_skus
        
        vals['product_id'] = self._check_and_set_product(product_id, product_skus)
        res = super(ProdPricelistItems, self).write(vals)
        # do some writes
        self._add_update_pricelist_items()
        return res

    def _get_attribute_price(self, att_value_ids):
        if any(atts.id == self.prices_id.attribute1_id.id for atts in att_value_ids):
            return {'att_id': self.prices_id.attribute1_id.id, 'price': self.attribute1_price, 'price_1': self.att1_price_1, 'price_2': self.att1_price_2}
        elif any(atts.id == self.prices_id.attribute2_id.id for atts in att_value_ids):
            return {'att_id': self.prices_id.attribute2_id.id, 'price': self.attribute2_price, 'price_1': self.att2_price_1, 'price_2': self.att2_price_2}
        elif any(atts.id == self.prices_id.attribute3_id.id for atts in att_value_ids):
            return {'att_id': self.prices_id.attribute3_id.id, 'price': self.attribute3_price, 'price_1': self.att3_price_1, 'price_2': self.att3_price_2}
        elif any(atts.id == self.prices_id.attribute4_id.id for atts in att_value_ids):
            return {'att_id': self.prices_id.attribute4_id.id, 'price': self.attribute4_price, 'price_1': self.att4_price_1, 'price_2': self.att4_price_2}
        elif any(atts.id == self.prices_id.attribute5_id.id for atts in att_value_ids):
            return {'att_id': self.prices_id.attribute5_id.id, 'price': self.attribute5_price, 'price_1': self.att5_price_1, 'price_2': self.att5_price_2}
        elif any(atts.id == self.prices_id.attribute6_id.id for atts in att_value_ids):
            return {'att_id': self.prices_id.attribute6_id.id, 'price': self.attribute6_price, 'price_1': self.att6_price_1, 'price_2': self.att6_price_2}
        elif any(atts.id == self.prices_id.bib_attribute_id.id for atts in att_value_ids):
            return {'att_id': self.prices_id.bib_attribute_id.id, 'price': self.bib_price_discount, 'price_1': 0, 'price_2': 0}
        else:
            return {'att_id': False, 'price': self.retail_price, 'price_1': 0, 'price_2': 0}

    def _check_and_set_product(self, product_id, skus):
        if product_id:
            return product_id
        prodTemplate = self.env['product.template'].search([])
        if skus:
            prod_ids = prodTemplate.filtered(lambda p: set(self._striplist(str(p.product_skus).split('/'))) & set(self._striplist(str(skus).split('/'))))
            if prod_ids:
                return prod_ids[0].id
                
    def _striplist(self, list):
        return ([x.strip() for x in list if x.strip()])
    
    def _add_update_pricelist_items(self):
        Pricelist = self.env['product.pricelist']
        Product = self.env['product.product']
        ProductPrice = self.env['product.attribute.price']
        plList = Pricelist.search([('id', 'in', self.prices_id.pricelist_id.ids)])  
        #self.prices_id.pricelist_id
        ppList = Product.search([('product_tmpl_id', '=', self.product_id.id)])
        
        if not self.product_id:
            return
        val = {'list_price': self.retail_price}
        if self.hardware_discount:
            val['hardware_discount'] = self.hardware_discount
        if self.taxable_amount:
            val['taxable_amount'] = self.taxable_amount
        self.product_id.write(val)
        
        
        #Loop through the available Pricelists
        for pp in ppList:
            for pl in plList:
                #Add or update the Bring it Back option
                bibId = self.prices_id.bib_attribute_id.id
                if any(atts.id == bibId for atts in pp.attribute_value_ids):
                    bibPrice = self.bib_price_discount * -1
                else:
                    bibPrice = 0
                item = pl.item_ids.filtered(lambda x: x.product_id.id == pp.id)
                #(['&', ('product_id', '=', pp.id), ('pricelist_id', '=', pp.id)])
                fixedPrice = self._get_attribute_price(pp.attribute_value_ids)
                finalFixedPrice = (0 if fixedPrice['price'] + bibPrice < 0 else fixedPrice['price'] + bibPrice)
                taxable = self.taxable_amount if self.taxable_amount else finalFixedPrice
                per_month = fixedPrice['price_1'] + round((0 if fixedPrice['price'] + bibPrice >= 0 else fixedPrice['price'] + bibPrice)/24, 2)
                final_per_month = (0 if per_month < 0 else per_month)
                if item:
                    item.write({'fixed_price': finalFixedPrice, 'price_1': final_per_month, 'price_2': fixedPrice['price_2']})
                
                else:
                    self.env['product.pricelist.item'].create({
                        'fixed_price': finalFixedPrice,
                        'product_id': pp.id,
                        'applied_on': '0_product_variant',
                        'compute_price': 'fixed',
                        'pricelist_id': pl.id,
                        'price_1': final_per_month,
                        'price_2': fixedPrice['price_2']
                    })
                    
                if not pp.product_tmpl_id.taxable_product_id:
                    new_template = pp.product_tmpl_id.create({
                        'name': 'Taxable - ' + pp.product_tmpl_id.name,
                        'active': True,
                        'image': pp.product_tmpl_id.image,
                        'image_medium': pp.product_tmpl_id.image_medium,
                        'sale_ok': True,
                        'website_published': False
                    })
                    pp.product_tmpl_id.write({'taxable_product_id': new_template.id})
                else:
                    new_template = pp.product_tmpl_id.taxable_product_id
                    
                tmpl_exists = pl.item_ids.filtered(lambda x: x.product_tmpl_id.id == new_template.id)
                if tmpl_exists:
                    if tmpl_exists[0].fixed_price != taxable:
                        tmpl_exists[0].write({'fixed_price': taxable})
                else:
                    pl.item_ids.create({
                        'fixed_price': taxable,
                        'product_tmpl_id': new_template.id,
                        'applied_on': '1_product',
                        'compute_price': 'fixed',
                        'pricelist_id': pl.id
                    })
        #pap = ProductPrice.search(['&', ('value_id', '=', bibId), ('product_tmpl_id', '=', self.product_id.id)])
        #if pap:
        #    pap.write({'price_extra': bibPrice })
        #else:
        #    ProductPrice.create({'product_tmpl_id': self.product_id.id, 'value_id': bibId, 'price_extra': bibPrice})
            
        #Loop through the product.product items to update the product.attribute.prices and add to the Pricelist.
        #for pp in ppList:
        #    attPrice = self._get_attribute_price(pp.attribute_value_ids)
        #    price = attPrice['price'] - self.retail_price
        #    pap = ProductPrice.search(['&', ('value_id', '=', attPrice['att_id']), ('product_tmpl_id', '=', pp.product_tmpl_id.id)])
        #    if pap:
        #        pap.write({'price_extra': price})
        #    else:
        #        ProductPrice.create({'product_tmpl_id': pp.product_tmpl_id.id, 'value_id': attPrice['att_id'], 'price_extra': price})
            
            #Add, Update, or remove a Pricelist item if the price is negative
        #    if attPrice['att_id'] != bibId and any(attId.id == bibId for attId in pp.attribute_value_ids):
        #        for pl in plList:
        #            item = pl.item_ids.search(['&', ('product_id', '=', pp.id), ('pricelist_id', '=', pl.id)])
        #            bibPrice = attPrice['price'] - self.bib_price_discount

        #            if item:
        #                if 0 > bibPrice != item.fixed_price:
        #                    item.write({'fixed_price': 0})
        #                elif bibPrice >= 0:
        #                    item.unlink()
        #            elif bibPrice <= 0:
        #                self.env['product.pricelist.item'].create({
        #                    'fixed_price': 0,
        #                    'product_id': pp.id,
        #                    'applied_on': '0_product_variant',
        #                    'compute_price': 'fixed',
        #                    'pricelist_id': pl.id
        #                })


class ProductTemplate(models.Model):
    _inherit = "product.template"

    hardware_discount = fields.Float('Hardware Discount', default=0, digits=(16, 2))
    taxable_amount = fields.Float('Taxable Amount', default=0, digits=(16, 2))
    product_skus = fields.Char("Product Sku's")
    taxable_product_id = fields.Many2one('product.template', 'Taxable Product')
    
    
class product_pricelist(models.Model):
    _inherit = "product.pricelist.item"
    
    price_1 = fields.Float(string='Custom Price 1')
    price_2 = fields.Float(string='Custom Price 2')
    taxable_amount = fields.Float('Taxable Amount', default=0, digits=(16, 2))
