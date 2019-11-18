# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import babel
import json
import logging
from werkzeug.exceptions import Forbidden, NotFound
from datetime import datetime, timedelta, time
from odoo import fields, http, tools, _
from odoo.http import request
from odoo.addons.website_sale_options.controllers.main import WebsiteSaleOptions

_logger = logging.getLogger(__name__)

"""
class WebsiteDealerInfo(http.Controller):
    
    def get_dealer_info_ids(self):
        "" list of active selectable dealer info

        :return: list of dealer info
           ()
        ""
        # dealer info
        dealer_info = http.request.env['dealer.info']
        dealers = dealer_info.search(['is_active', '=', 'true'])
        return  dealers


        
    # ------------------------------------------------------
    # TELUS Redirect
    # ------------------------------------------------------
    ""
    def telus_redirection(self, order):
        # must have a draft sales order with lines at this point, otherwise reset
        if not order or order.state != 'draft':
            request.session['sale_order_id'] = None
            request.session['sale_transaction_id'] = None
            return request.redirect('/shop')

        if order and not order.order_line:
            return request.redirect('/shop/cart')

        # if transaction pending / done: redirect to confirmation
        tx = request.env.context.get('website_sale_transaction')
        if tx and tx.state != 'draft':
            return request.redirect('/shop/payment/confirmation/%s' % order.id)
    ""
    @http.route('/telus/<model("dealer.info"):dealer>', auth='user')
    def telus_redirect(self, dealer):
        if self.env.user != SUPERUSER_ID:
            self.env.user.dealer_info_id = dealer
        websettings = self.pool.get('sale.config.settings').browse(cr,uid,ids)[0]
        response = redirect("https://evs.telus.com/evs?channel_id=" + websettings.channel_id + "&amp;campaign_id=" + websettings.campaign_id + "&amp;RCID=" + dealer.rcid)
        return response
"""
	
class InheritWebsiteSaleOptions(WebsiteSaleOptions):	

    @http.route(['/shop/cart/update_option'], type='http', auth="public", methods=['POST'], website=True, multilang=False)
    def cart_options_update_json(self, product_id, add_qty=1, set_qty=0, goto_shop=None, lang=None, **kw):
        res = super(InheritWebsiteSaleOptions, self).cart_options_update_json(
            product_id=product_id, 
            add_qty=add_qty, 
            set_qty=set_qty, 
            lang=lang,
            **kw
	)
        _logger.info('*** Inside the custom update option')	
        
        product = request.env['product.product'].browse(int(product_id))

        attributes = self._filter_attributes(**kw)
        
        order = request.website.sale_get_order()
	
        # add a taxable line
        if product.taxable_product_id:
            tax_lines = order.sudo().order_line.filtered(lambda x: x.product_id.id == int(product.taxable_product_id.id))
            tax_linked_ids = [x.linked_line_id for x in tax_lines]
            prod_lines = order.sudo().order_line.filtered(lambda x: x.id not in tax_linked_ids and x.product_id.id == int(product_id) and x.product_id.product_tmpl_id.taxable_product_id and x.product_id.product_tmpl_id.taxable_product_id.id == product.taxable_product_id.id)
            taxable = request.env['product.product'].sudo().search([('product_tmpl_id', '=', product.taxable_product_id.id)], limit=1)
            for i in prod_lines:
                order._cart_update(
                    product_id=int(taxable.id),
                    set_qty=i.product_uom_qty,
                    attributes=attributes,
                    linked_line_id=i.id
                )
	
        return str(order.cart_quantity)
