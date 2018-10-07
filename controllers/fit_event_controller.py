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
                        _logger.info('Deleting registration')
                        registration.unlink()
                        subscription_update_counter += 1
        else:
            _logger.info('Creating registration')
            http.request.env['event.registration'].sudo().create(
                {'partner_id': partner_id,
                 'event_id': event_id}
            )
            subscription_update_counter -= 1

        self._update_counter_subscription(event, partner, subscription_update_counter)

        return http.request.redirect('/event')

    def _update_counter_subscription(self, event, partner, subscription_update_counter):
        event_cat = str(event.event_type_id.name).lower()
        cf_montly = http.request.env['fit.subscription'].sudo().search([('subscription_type', '=', 'cf_montly')])
        bc_montly = http.request.env['fit.subscription'].sudo().search([('subscription_type', '=', 'bc_montly')])
        bc_tickets = http.request.env['fit.subscription'].sudo().search([('subscription_type', '=', 'bc_tickets')])
        bz_tickets = http.request.env['fit.subscription'].sudo().search([('subscription_type', '=', 'bz_tickets')])

        if event_cat == 'bokszak':
            if bz_tickets and bz_tickets.subscription_is_active:
                bz_tickets.subscription_counter += subscription_update_counter

        if event_cat == 'bootcamp':
            if bc_montly and bc_montly.subscription_is_active:
                return
            if cf_montly and cf_montly.subscription_is_active:
                return
            if bc_tickets and bc_tickets.subscription_is_active:
                bc_tickets.subscription_counter += subscription_update_counter