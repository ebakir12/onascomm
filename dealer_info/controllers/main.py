# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import babel
import werkzeug

from datetime import datetime, timedelta, time

from odoo import fields, http, SUPERUSER_ID, _
from odoo.http import request

class WebsiteDealerInfo(http.Controller):
    
    def get_dealer_info_ids(self):
        """ list of active selectable dealer info

        :return: list of dealer info
           ()
        """
        # dealer info
        dealer_info = http.request.env['dealer.info']
        dealers = dealer_info.search(['is_active', '=', 'true'])
        return  dealers


        
    # ------------------------------------------------------
    # TELUS Redirect
    # ------------------------------------------------------
    """
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
    """
    @http.route('/telus/<model("dealer.info"):dealer>', auth='public')
    def telus_redirect(self, dealer):
        user = request.env.user
        values = {}
        values['dealer_info_id'] = dealer.id
        user.sudo().write(values)
        websettings = http.request.env['res.config.settings'].sudo().get_values()
        url = "https://evs.telus.com/evs?channel_id=" + websettings['channel_id'] + "&campaign_id=" + websettings['campaign_id'] + "&RCID=" + dealer.rcid
        return werkzeug.utils.redirect(url)

    """
        Page called when the user successfully completes the TELUS registration
    """
    @http.route('/telus/welcome', type='http', auth="public", website=True)
    def telus_welcome(self, **kwargs):
        user = request.env.user
        values = {}
        values['property_product_pricelist'] = user.dealer_info_id.pricelist_id
        if 'program_code' in kwargs:
            values['telus_program_code'] = kwargs['program_code']
        if 'activation_code' in kwargs:
            values['telus_activation_code'] = kwargs['activation_code']
        if 'program_code' in kwargs:
            values['language'] = kwargs['language']
        if 'token' in kwargs:
            values['telus_token'] = kwargs['token']
        user.sudo().write(values)
        return http.request.render('dealer_info.telus_welcome', {})
