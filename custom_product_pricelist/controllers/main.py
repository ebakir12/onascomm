# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging
from werkzeug.exceptions import Forbidden, NotFound

from odoo import http, tools, _
from odoo.http import request


class WebsitePricelist(http.Controller):
    
    """
	def get_dealer_info_ids(self):
        """ list of active selectable dealer info

        :return: list of dealer info
           ()
        """
        # dealer info
        dealer_info = http.request.env['dealer_info.dealerinfo']
        return  dealer_info.search(['is_active', '=', 'true'])
	"""

        
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