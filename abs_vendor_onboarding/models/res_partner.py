# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api,fields,models,_

class Partner(models.Model):
    _inherit = "res.partner"

    commercial_name = fields.Char(string="Commercial Name")
    attachment_ids = fields.One2many('ir.attachment', 'partner_id', string='Attachments')


class Attachment(models.Model):
    _inherit = "ir.attachment"

    partner_id = fields.Many2one('res.partner', string="Partner")
