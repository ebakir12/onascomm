# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import babel
import werkzeug
import logging
import urllib.request as req
import json

from datetime import datetime, timedelta, time

from odoo import fields, http, SUPERUSER_ID, _
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

class ProductManagement(http.Controller):
    
     
    # ------------------------------------------------------
    # Product Export
    # ------------------------------------------------------
    @http.route(['/json/product/<int:product>'], auth='none', type='json', csrf=False, method=['POST'])
    def post_product(self, product, **kw):
        #_logger.debug('*** Product ID: %s', product.id)
        _logger.debug('*** params list: %s', kw)
        template = http.request.env['product.template'].search([('id', '=', product)], limit=1)
        variants = http.request.env['product.product'].search([('product_tmpl_id', '=', product)])
        colours = kw['colours']
        count = 0
        for colour in colours:
            if 'image_medium' not in colour:
                continue
            c = http.request.env['product.attribute.value'].search([('attribute_id.name', '=', 'Colour')]).filtered(lambda x: x.name.lower() == colour['colour'].lower())
            #, ('lower(name)', '=', lower(colour['colour'])
            vlist = variants.filtered(lambda x: c.id in x.attribute_value_ids.ids)
            for variant in vlist:
                count = count + 1
                variant.sudo().write({"image_variant": colour['image_medium']})
        """
        variants = http.request.env['product.product'].search([('product_tmpl_id', '=', tmpl.id)])
        _logger.debug('*** Variants list: %s', variants)
        colours = tmpl.attribute_value_ids.filtered(lambda x: x.attribute_id.name == 'Colour')
        _logger.debug('*** Colours list: %s', colours)
        product_colours = []
        for c in colours:
            single_colour = variants.filtered(lambda x: c.id in x.atribute_value_ids)
            product_colours.append({"colour":c.name, "image_medium": single_colour[0].image_medium})
        product = {
            "name":tmpl.name,
            "colours": product_colours
        }
        headers = {'Content-Type': 'application/json'}
        body = { 'results': { 'code':200, 'message':'OK' } }
        """
        
        Response.status = '200'
        return json.dumps({"count":count})
    #, content_type='application/json;charset=utf-8',status=200)

    # ------------------------------------------------------
    # Product Export
    # ------------------------------------------------------
    @http.route(['/json/getproduct/<int:product>'], auth='none', type='json')
    def get_product(self, product, **kw):
        #_logger.debug('*** Product ID: %s', product.id)
        _logger.debug('*** params list: %s', kw)
        template = http.request.env['product.template'].search([('id', '=', product)], limit=1)
        variants = http.request.env['product.product'].search([('product_tmpl_id', '=', product)])
        _logger.debug('*** Variants list: %s', variants)
        colours = template.attribute_line_ids.filtered(lambda x: x.attribute_id.name == 'Colour')
        #colours = template.attribute_value_ids.filtered(lambda x: x.attribute_id.name == 'Colour')
        _logger.debug('*** Colours list: %s', colours)
        product_colours = []
        for c in colours[0].value_ids:
            #col = c.value_ids.filtered(lambda x: x.attribute_id.name == 'Colour')
            single_colour = variants.filtered(lambda x: c.id in x.attribute_value_ids.ids)
            product_colours.append({"colour":c.name, "image_medium": single_colour[0].image.decode('UTF-8')})
        product = {
            "name":template.name,
            "colours": product_colours
        }
        headers = {'Content-Type': 'application/json'}
        body = { 'results': { 'code':200, 'message':'OK' } }
        
        
        Response.status = '201'
        return json.dumps(product)
    #, content_type='application/json;charset=utf-8',status=200)
