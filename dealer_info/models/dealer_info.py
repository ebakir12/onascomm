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
    dealer_image = fields.Binary(string='Dealer Image')
    welcome_text = fields.Text(string='Welcome Text')

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

class product_pricelist(models.Model):
    _inherit = "product.pricelist.item"
    
    price_1 = fields.Float(string='Custom Price 1')
    price_2 = fields.Float(string='Custom Price 2')

    
class sales_order(models.Model):
    _inherit = "sale.order"
    
    partner_user_id = fields.Many2one('res.users', string='Partner User Id')
    dealer_info = fields.Char(related='partner_user_id.dealer_info_id.name', string="Dealer Organization")
    dealer_info_rcid = fields.Char(related='partner_user_id.dealer_info_id.rcid', string="RCID")
    user_id_activation_code = fields.Char(related='partner_user_id.telus_activation_code', string="Activation Code")
    partner_id_phone = fields.Char(related='partner_id.phone', string="Phone")
    partner_id_email = fields.Char(related='partner_id.email', string="Email")
    
    @api.model
    def create(self, data):
        user_id = self.env['res.users'].sudo().search([('partner_id', '=', data['partner_id'].id)], limit=1)
        if user_id:
            data['partner_user_id'] = user_id.id
        res = super(sales_order, self).create(data)        
        return res
