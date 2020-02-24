# -*- coding: utf-8 -*-

from odoo import models, fields, api


class partner_extended(models.Model):
    _inherit = 'res.partner'
    #_description = 'partner extended'
    
    
    is_customer = fields.Boolean(string="Is customer")
    is_vendor = fields.Boolean(string="Is vendor")
    