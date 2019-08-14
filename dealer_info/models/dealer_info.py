# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models

class DealerInfo(models.Model):
    _name = "dealer.info"
    
    name = fields.Char(string='Organization Name', required=True)
    rcid = fields.Char(string='RCID or COINS')
    dealer_url = fields.Char(string='Dealer URL')
    contact_email = fields.Char(string='Internal Contact')
    is_active = fields.Boolean(string='Active')
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')

    # @api.model
    # def create(self, data):
    #     res = super(DealerInfo, self).create(data)
    #     self.clear_cache()
    #     return res

    # @api.multi
    # def write(self, data):
    #     res = super(DealerInfo, self).write(data)
    #     self.clear_cache()
    #     return res
    
class res_users(models.Model):
    _inherit = "res.users"
    
    dealer_info_id = fields.Many2one('dealer.info', string='EPP Business')
    telus_program_code = fields.Char(string='Telus Program Code')
    telus_activation_code = fields.Char(string='Telus Activation Code')
    telus_language = fields.Char(string='Telus Selected Language')
    telus_token = fields.Char(string='Telus Token')

class product_pricelist(models.Model):
    _inherit = "product.pricelist"
    
    telus_discount_image = fields.Binary(string='Discount Image')
