import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class FitEventSubscription(models.Model):
    _name = 'fit.subscription'
    _description = 'Inschrijving'

    subscription_partner = fields.Many2one(comodel_name='res.partner', string='Inschrijving-Partner')
    subscription_is_active = fields.Boolean(compute='_is_active')
    subscription_start = fields.Date('Start inschrijving')
    subscription_end = fields.Date('Einde inschrijving')
    subscription_counter = fields.Integer('Strippenkaart')
    subscription_category = fields.Char()
    subscription_type = fields.Selection([('cf_montly', 'Maandelijks (Crossfit)'),
                                          ('bc_montly', 'Maandelijks (Bootcamp)'),
                                          ('bc_tickets', 'Strippenkaart (Bootcamp)'),
                                          ('bz_tickets', 'Strippenkaart (Bokszak)')])

    @api.one
    def _is_active(self):
        if self.subscription_type:
            _type = self.get_subscription_type(self.subscription_type)
            if _type == 'subscription':
                end_date = datetime.strptime(self.subscription_end, '%Y-%m-%d').date()
                start_date = datetime.strptime(self.subscription_start, '%Y-%m-%d').date()
                present = datetime.now().date()
                if present < start_date or present > end_date:
                    self.subscription_is_active = False
                else:
                    self.subscription_is_active = True
            if _type == 'tickets':
                if self.subscription_counter > 0:
                    self.subscription_is_active = True
                else:
                    self.subscription_is_active = False

    @api.onchange('subscription_start')
    def on_change_start(self):
        if self.subscription_type:
            dt = datetime.strptime(self.subscription_start, '%Y-%m-%d') + relativedelta(months=+1)
            self.subscription_end = dt

    @api.onchange('subscription_type')
    def on_change_type(self):
        if self.subscription_type:
            if self.subscription_type == 'cf_montly':
                self.subscription_category = 'crossfit'
            if self.subscription_type == 'bc_montly' or self.subscription_type == 'bc_tickets':
                self.subscription_category = 'bootcamp'
            if self.subscription_type == 'bz_tickets':
                self.subscription_category = 'bokszak'

    def get_subscription_type_length(self, product, invoice_line):
        given_type = product.fit_subscription_type
        if self.get_subscription_type(given_type) == 'subscription':
            return int(invoice_line.quantity)
        else:
            if self.get_subscription_type(given_type) == 'tickets':
                return int(invoice_line.quantity) * 10
        return 0

    def get_subscription_type(self, given_type):
        type_type = {
            'cf_montly': 'subscription',
            'bc_montly': 'subscription',
            'bc_tickets': 'tickets',
            'bz_tickets': 'tickets',
        }
        return type_type.get(given_type, '')

    def _can_subscribe(self, event_type):
        event_cat = str(event_type.name).lower()
        type = self.get_subscription_type(self.subscription_type)
        if not self.subscription_category:
            self.on_change_type()
        sub_cat = str(self.subscription_category).lower()
        if sub_cat == 'crossfit' and type == 'subscription' and event_cat == 'bootcamp':
            event_cat = 'crossfit'
        if sub_cat == event_cat:

            if type == 'subscription':
                present = datetime.now().date()
                start = datetime.strptime(self.subscription_start, '%Y-%m-%d').date()
                end = datetime.strptime(self.subscription_end, '%Y-%m-%d').date()

                if start <= present and end >= present:
                    _logger.info('Montly subscription, can subscribe event_cat: %s, sub_cat: %s, start %s, end %s, present %s', event_cat,
                                 sub_cat, start, end, present)
                    return True

            if type == 'tickets':
                if self.subscription_counter > 0:
                    _logger.info('Ticket subscription, can subscribe event_cat: %s, sub_cat: %s', event_cat, sub_cat)
                    return True

    def update(self, product, payment_type, invoice_line):
        _logger.info('Updating subscription: ' + str(payment_type))

        if (product.fit_subscription_type == self.subscription_type):
            subscription_extension = self.get_subscription_type_length(product, invoice_line)

            if self.get_subscription_type(self.subscription_type) == 'subscription':

                if payment_type == 'inbound':
                    present = datetime.now().date()
                    current_end_date = datetime.strptime(self.subscription_end, '%Y-%m-%d').date()

                    if present > current_end_date:
                        new_end_date = present + relativedelta(months=+subscription_extension)
                    else:
                        new_end_date = current_end_date + relativedelta(months=+subscription_extension)
                    self.subscription_end = new_end_date
                    return True
                else:
                    if payment_type == 'outbound':
                        new_end_date = datetime.strptime(self.subscription_end, '%Y-%m-%d') + relativedelta(months=-subscription_extension)
                        present = datetime.now().date()

                        if present > new_end_date.date():
                            self.subscription_end = present + relativedelta(days=-1)
                        else:
                            self.subscription_end = new_end_date
                        return True
            else:
                if self.get_subscription_type(self.subscription_type) == 'tickets':

                    if payment_type == 'inbound':
                        self.subscription_counter += subscription_extension
                        return True
                    else:
                        if payment_type == 'outbound':
                            new_subscription_counter = self.subscription_counter - subscription_extension

                            if new_subscription_counter < 0:
                                new_subscription_counter = 0
                            self.subscription_counter = new_subscription_counter
                            return True
        return False
