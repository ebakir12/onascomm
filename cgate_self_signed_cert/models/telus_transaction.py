# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
import requests
import json
import logging
import xml.etree.ElementTree as ET

_logger = logging.getLogger(__name__)

class ResourcePartnerInherit(models.Model):
    _inherit = 'res.partner'

    ban = fields.Char(string='Ban')

class TelusTransaction(models.Model):
    _name = "telus.transaction"

    ssl_cert_id = fields.Many2one('ssl.cert', 'Certificate', required=True,
                                  default=lambda self: self._compute_default_cert())
    serial_no = fields.Char(string='Serial Number')
    e_transaction = fields.Char(string='E Transaction Id')
    ban = fields.Char(string='BAN')
    subscription_mdn = fields.Char(string='Subscription MDN')
    customer_id = fields.Many2one('res.partner', 'Customer')
    product_ids = fields.Many2many('product.product', 'telus_products_rel', string='Telus Products')
    payload = fields.Text(string='SOAP Response')

    def _compute_default_cert(self):
        return self.env['ssl.cert'].search([('is_active', '=', True)], limit=1)

    @api.multi
    def create_from_ui(self, serial_no):
        val = self.env['telus.transaction'].create({'serial_no': serial_no})
        return {'id': val.id,
                'product_ids': val.product_ids.ids,
                'customer_id': val.customer_id.id}

    @api.model
    def create(self, vals):
        # vals['product_ids'] = [(6, 0, [10,17] )]
        # data['product_ids'] = [(6, 0, [10,37] )]
        res = super(TelusTransaction, self).create(vals)
        res.write({
            'payload': self._telus_soap_call(res)
        })
        return res

    def _telus_soap_call(self, res):
        cert = res.ssl_cert_id
        if not cert.url:
            return 'URL is not specified'
        url = str(cert.url)  # "https://api.preprd.teluslabs.net"
        endpoint = str(cert.endpoint)  # "/soap/v1/salesInfo_vs0"
        cert_loc = "src/user/cgate_self_signed_cert/cert"
        key_loc = "src/user/cgate_self_signed_cert/key"
        client_key = key_loc + '/' + cert.name + '_client_key.key'
        server_cert = cert_loc + '/' + cert.name + '_server_cert.crt'
        headers = {'X-Telus-SDF-Developer-Key': cert.developer_key}
        request = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:typ="http://schemas.telus.com/partnerIntegration/Transaction_RequestResponse_1_0/types" xmlns:par="http://schemas.telus.com/partner">
           <soapenv:Header/>
           <soapenv:Body>
              <typ:getTransactionRequest>
                 <typ:requestor>
                    <par:channelOrgNo>{}</par:channelOrgNo>
                    <par:outletCode>{}</par:outletCode>
                    <par:externalUserId>{}</par:externalUserId>
                 </typ:requestor>
                 <!--You have a CHOICE of the next 4 items at this level-->
                 <!--Optional:-->
                 <typ:serialNo>{}</typ:serialNo>
                 <!--Optional:-->
                 <!--<typ:eTransactionId>{}</typ:eTransactionId>-->
                 <!--Optional:-->
                 <!--<typ:ban>{}</typ:ban>-->
                 <!--Optional:-->
                 <!--<typ:subscriberMdn>{}</typ:subscriberMdn> -->
              </typ:getTransactionRequest>
           </soapenv:Body>
        </soapenv:Envelope>""".format(cert.channel_org, cert.outlet_code, cert.user_id_ext, res.serial_no,
                                      res.e_transaction, res.ban, res.subscription_mdn)
        r = requests.post(url=url + endpoint, data=request.encode('utf-8'), headers=headers,
                          cert=(server_cert, client_key))
        etstring = ET.fromstring(r.text)
        ns = {'ns1': 'http://schemas.telus.com/partnerIntegration/Transaction_RequestResponse_1_0/types'}
        ban = etstring.findall(".//ns1:ban", ns)
        if ban:
            _logger.info('*** Ban value: %s', ban[0].text)
            partner = self.env['res.partner'].search([('ban', '=', ban[0].text)], limit=1)
            _logger.info('*** Partner: %s', partner)
            if partner:
                rp = partner
            else:
                _logger.info('*** Create a new partner: %s', ban[0].text)
                fname = etstring.findall(".//ns1:contactFirstName", ns)
                lname = etstring.findall(".//ns1:contactLastName", ns)
                stnum = etstring.findall(".//ns1:streetNumber", ns)
                stname = etstring.findall(".//ns1:streetName", ns)
                city = etstring.findall(".//ns1:cityTown", ns)
                province = etstring.findall(".//ns1:province", ns)
                country = etstring.findall(".//ns1:country", ns)
                postalcode = etstring.findall(".//ns1:postalCode", ns)
                _logger.info('*** Create a new partner: %s %s', fname[0].text, lname[0].text)
                rp = partner.create({
                    'company_type': 'person',
                    'name': fname[0].text + ' ' + lname[0].text,
                    'street': stnum[0].text + ' ' + stname[0].text,
                    'city': city[0].text,
                    'zip': postalcode[0].text,
                    'ban': ban[0].text
                })
            res.write({'customer_id': rp.id})
        return ET.tostring(etstring).decode()  # , encoding='utf8', method='xml') #r.content.decode('utf-8')
