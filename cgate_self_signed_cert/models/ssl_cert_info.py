# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from OpenSSL import crypto, SSL
import os


class SelfSignedCert(models.Model):
    _name = "ssl.cert"

    name = fields.Char(string='Certificate Name', required=True)
    is_active = fields.Boolean('Active')
    channel_org = fields.Char(string='Channel Org Number')
    outlet_code = fields.Char(string='Outlet Code')
    user_id_ext = fields.Char(string='External User Id')
    name_c = fields.Char(string='Country Name', size=2, help="Country Name in 2 Characters. Canada would be 'CA'")
    name_st = fields.Char(string='State or Province Name', help="London")
    name_l = fields.Char(string='Locality Name', help="London")
    name_o = fields.Char(string='Organization Name', help="Sample Org LTD.")
    name_ou = fields.Char(string='Organization Unit Name', help="Sample Org LTD.")
    name_cn = fields.Char(string='Common Name', help="www.example.com")
    name_email = fields.Char(string='Email Address', help="sample@email.com")
    cert_client = fields.Char(string='Client Certificate')
    cert_key = fields.Char(string='Client Key')
    cert_server = fields.Char(string='Server Certificate')

    @api.model
    def create(self, data):
        res = super(SelfSignedCert, self).create(data)
        if res.cert_client is not None and res.cert_key is not None:
            self._write_files(res.cert_client, res.cert_key, res.cert_server, res.name)
        else:
            self._create_self_signed_cert(data)
        
        return res

    @api.multi
    def write(self, data):
        res = super(SelfSignedCert, self).write(data)
        if res.cert_client is not None and res.cert_key is not None:
            self._write_files(res.cert_client, res.cert_key, res.cert_server, res.name)
        
        return res

    def _write_files(self, client_cert, client_key, server_cert, file_name):
        cert_loc = "src/user/cgate_self_signed_cert/cert"
        key_loc = "src/user/cgate_self_signed_cert/key"
        self._write_file(cert_loc, file_name, client_cert, '_client_cert.crt')
        self._write_file(key_loc, file_name, client_key, '_client_key.key')
        self._write_file(cert_loc, file_name, server_cert, '_server_cert.crt')
                
    def _write_file(self, file_path, file_name, file_content, file_type):
        if not os.path.exists(file_path):
            os.mkdir(file_path)
            
        if file_content:
            file_name = str(file_name) + str(file_type)
            with open(os.path.join(file_path, file_name), 'w') as f:
                f.write(file_content)

    def _create_self_signed_cert(self, data):
        # Creating a Key Pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)

        # Create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = data.name_c
        cert.get_subject().ST = data.name_st
        cert.get_subject().L = data.name_l
        cert.get_subject().O = data.name_o
        cert.get_subject().OU = data.name_ou
        cert.get_subject().CN = data.name_cn
        cert.get_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, b'shal')

        self._write_files(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode(),
                     crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode(), False, data.name)
