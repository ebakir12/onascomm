# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval

from odoo import api, fields, models
from odoo.exceptions import AccessDenied


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _default_website(self):
        return self.env['website'].search([], limit=1)

    channel_id = fields.Char(string='Channel ID')
    campaign_id = fields.Char(string='Campaign ID')

    

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            channel_id=get_param('channel_id', default=''),
            campaign_id=get_param('campaign_id', default=''),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('channel_id', (self.channel_id or '').strip())
        set_param('campaign_id', (self.campaign_id or '').strip())