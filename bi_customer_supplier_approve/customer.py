# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import Warning

class ResPartner(models.Model):
    _inherit = 'res.partner'

    unique_code = fields.Char('ID', readonly=True)
    state = fields.Selection([
                ('new', 'New'),
                ('confirm', 'Confirm'),
                ('approve', 'Approved'),
            ], 'Stage', readonly=True, default="new")

    @api.model
    def create(self, vals):
        vals['unique_code'] = self.env['ir.sequence'].next_by_code('res.partner.unique.code') or 'New'
        result = super(ResPartner, self).create(vals)
        return result

    def approve_partner(self):
        self.state = 'approve'
        return True

    def confirm_partner(self):
        self.state = 'confirm'
        return True
