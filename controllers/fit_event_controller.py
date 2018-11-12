# -*- coding: utf-8 -*-
# Copyright 2018 Fundament IT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, http, _
_logger = logging.getLogger(__name__)


class WebsiteEventController(http.Controller):

    @http.route(['/fit_subscribe_controller/subscribe'], type='http', auth="public", website=True)
    def event_register(self, **post):
        event_id = int(post[u'event_id'])
        event_is_participating = post[u'event_is_participating']
        event = http.request.env['event.event'].sudo().browse(event_id)
        subscription_update_counter = 0

        partner = http.request.env.user.partner_id
        partner_id = int(partner.id)
        if event_is_participating:
            for registration in event.registration_ids:
                for partner in registration.partner_id:
                    if partner.id == partner_id:
                        _logger.info('Found existing registration, set state to cancelled.')
                        #registration.unlink()
                        registration.state = 'cancel'
                        subscription_update_counter += 1
        else:
            #_logger.info('Search existing registration')
            existing_registration = http.request.env['event.registration'].sudo().search([('partner_id', '=', partner_id),
                                                                                          ('event_id', '=', event.id)])
            if existing_registration:
                _logger.info('Found existing registration, set state to open (confirmed)')
                existing_registration.state = 'open'
            else:
                _logger.info('No registration found, create new one')
                http.request.env['event.registration'].sudo().create(
                    {
                        'partner_id': partner_id,
                        'event_id': event_id,
                        'name': partner.name if partner.name else '',
                        'phone': partner.mobile if partner.mobile else '',
                        'email': partner.email if partner.email else '',
                    }
                )
            subscription_update_counter -= 1

        self._update_counter_subscription(event, partner, subscription_update_counter)
        referer = str(http.request.httprequest.headers.environ['HTTP_REFERER'])
        return http.request.redirect(str('/'+referer.split('/')[-1]))

    def _update_counter_subscription(self, event, partner, subscription_update_counter):
        event_cat = str(event.event_type_id.name).lower()
        cf_monthly = http.request.env['fit.subscription'].sudo().search([('subscription_type', '=', 'cf_montly'),
                                                                        ('subscription_partner', '=', partner.id)])

        bc_monthly = http.request.env['fit.subscription'].sudo().search([('subscription_type', '=', 'bc_montly'),
                                                                        ('subscription_partner', '=', partner.id)])
        bc_tickets = http.request.env['fit.subscription'].sudo().search([('subscription_type', '=', 'bc_tickets'),
                                                                        ('subscription_partner', '=', partner.id)])
        bz_tickets = http.request.env['fit.subscription'].sudo().search([('subscription_type', '=', 'bz_tickets'),
                                                                        ('subscription_partner', '=', partner.id)])

        if event_cat == 'bokszak':
            if bz_tickets:
                bz_tickets.subscription_counter += subscription_update_counter

        if event_cat == 'bootcamp':
            if bc_monthly and bc_monthly.subscription_is_active:
                return
            if cf_monthly and cf_monthly.subscription_is_active:
                return
            if bc_tickets:
                bc_tickets.subscription_counter += subscription_update_counter
