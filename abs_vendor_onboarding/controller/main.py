# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import werkzeug
import json
import base64
import os

from odoo import http, _
from odoo.http import Controller, request, route


class WebsiteOnboardingForm(http.Controller):

    @http.route('/company_detail/submit', type="http", auth="user", website=True)
    def form_company_detail_submit(self, **post):
        partner = request.env.user.partner_id
        if partner and post.get('company_name') and post.get('rfc'):
            partner.sudo().write({'name' : post.get('company_name'), 'vat' : post.get('rfc')})
            return http.request.render('abs_vendor_onboarding.menu_onboarding')

    @http.route('/fiscal_address', type="http", auth="user", website=True)
    def form_fiscal_address(self, **kwargs):
        partner = request.env.user.partner_id
        value = {}
        values = {}
        value = kwargs
        state = 'state_id' in value and value['state_id'] != '' and request.env['res.country.state'].browse(int(value['state_id']))
        state = state and state.exists()
        state_province_ids = request.env['res.country.state'].sudo().search([])        

        country = 'country_id' in value and value['country_id'] != '' and request.env['res.country'].browse(int(value['country_id']))
        country = country and country.exists()
        country_ids = request.env['res.country'].sudo().search([])
        values = {
                  'country'                : country,
                  'country_ids'            : country_ids,
                  'state'                  : state,
                  'state_province_ids'     : state_province_ids,
                 }
        return http.request.render('abs_vendor_onboarding.form_fiscal_address', values)

    @http.route('/fiscal_address/submit', type="http", auth="public", website=True)
    def form_fiscal_address_submit(self, **post):
        partner = request.env.user.partner_id
        message = request.env['mail.message']
        if post.get('attachment', False):
            attachment_ids = []
            Attachments = request.env['ir.attachment']
            name = post.get('attachment').filename
            file = post.get('attachment')
            attachment = file.read()
            attachment_id = Attachments.sudo().create({'name':name,
                                                       'partner_id': partner.id,
                                                       'display_name': name,
                                                       'store_fname': name,
                                                       'res_name': name,
                                                       'type': 'binary',
                                                       'res_model': 'res.partner',
                                                       'res_id': partner.id,
                                                       'datas':base64.b64encode(attachment),
                                                     })
            attachment_ids.append(attachment_id.id)
            if attachment_ids:
                message_values ={
                                 'model': 'res.partner',
                                 'res_id': int(partner.id),
                                 'message_type': 'comment',
                                 'subtype_id': 1,
                                 'author_id' : request.env.user.partner_id.id,
                                 'attachment_ids' : [(6, 0, attachment_ids)]
                }
                message_new_obj = message.sudo().create(message_values)

        if partner:
            partner.sudo().write({'commercial_name' : post.get('commercial_name')})
            country_id = request.env['res.country'].search([('id', '=', post.get('country_id'))])
            partner_id = request.env['res.partner'].sudo().create({
                                                                   'name' : 'FISCAL ADDRESS',
                                                                   'type' : 'other',
                                                                   'company_type' : 'person',
                                                                   'parent_id' : partner.id,
                                                                   'street' : post.get('street'),
                                                                   'street2' : post.get('street2'),
                                                                   'city' : post.get('city'),
                                                                   'state_id' : post.get('state_id'),
                                                                   'zip' : post.get('postal_code'),
                                                                   'country_id' : country_id.id,
                                                                  })
        return http.request.render('abs_vendor_onboarding.menu_onboarding')
