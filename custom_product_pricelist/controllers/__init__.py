# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import babel

from datetime import datetime, timedelta, time

from odoo import fields, http, _
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
    @http.route('/telus/<model("dealer.info"):dealer>', auth='user')
    def telus_redirect(self, dealer):
        if self.env.user != SUPERUSER_ID:
            self.env.user.dealer_info_id = dealer
        websettings = self.pool.get('sale.config.settings').browse(cr,uid,ids)[0]
        response = redirect("https://evs.telus.com/evs?channel_id=" + websettings.channel_id + "&amp;campaign_id=" + websettings.campaign_id + "&amp;RCID=" + dealer.rcid)
        return response
