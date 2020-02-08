# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import werkzeug
import json
import base64
import os

from odoo import http, _
from odoo.http import Controller, request, route


class WebsiteOnboardingForm(http.Controller):

    def _prepare_portal_layout_values(self):
        # get customer sales rep
        sales_user = False
        partner = request.env.user.partner_id
        if partner.user_id and not partner.user_id._is_public():
            sales_user = partner.user_id

        return {
            'sales_user': sales_user,
            'page_name': 'home',
            'archive_groups': [],
        }

    @http.route('/company_detail/submit', type="http", auth="user", website=True)
    def form_company_detail_submit(self, **post):
        partner = request.env.user.partner_id
        if partner and post.get('company_name') and post.get('rfc'):
            partner.sudo().write({'name' : post.get('company_name'), 'vat' : post.get('rfc')})
            return http.request.render('abs_vendor_onboarding.menu_onboarding')

    @http.route('/fiscal_address', type="http", auth="user", website=True)
    def form_fiscal_address(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                values.update({'country_id': int(values.pop('country_id', 0))})
                values.update({'zip': values.pop('zipcode', '')})
                if values.get('state_id') == '':
                    values.update({'state_id': False})
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'commercial_name' : partner.company_name,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("abs_vendor_onboarding.form_fiscal_address", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @http.route('/company_detail', type="http", auth="user", website=True)
    def form_company_detail(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                values.update({'country_id': int(values.pop('country_id', 0))})
                values.update({'zip': values.pop('zipcode', '')})
                if values.get('state_id') == '':
                    values.update({'state_id': False})
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("abs_vendor_onboarding.form_company_detail_new", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

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
