import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class FitAccountPayment(models.Model):
    _name = "account.payment"
    _inherit = 'account.payment'

    @api.multi
    def post(self):
        super(FitAccountPayment, self).post()
        for record in self:
            payment_type = record.payment_type
            for invoice in record.invoice_ids:
                state = invoice.state
                partner = invoice.partner_id
                if state == 'paid':
                    for invoice_line in invoice.invoice_line_ids:
                        product = invoice_line.product_id
                        product_subscription_type = product.fit_subscription_type
                        if product_subscription_type:
                            self._update_fit_subscription(partner, product, payment_type, invoice_line)

    def _update_fit_subscription(self, partner, product, payment_type, invoice_line):
        updated = False
        for subscription in partner.fit_subscriptions:
            updated = subscription.update(product, payment_type, invoice_line)
            _logger.info('Updated subscription? ' + str(updated) + ', type: ' + product.fit_subscription_type)

        if not updated and payment_type == 'inbound':
            _logger.info('Not updated, create subscription for type: ' + product.fit_subscription_type)
            subscription_type = self.get_subscription_type(product.fit_subscription_type)
            subscription_length = self.get_subscription_type_length(product, invoice_line)

            if subscription_type == 'subscription':
                subscription_start = self._get_latest_subscription(partner)
                subscription_end = subscription_start + relativedelta(months=+subscription_length)
                self.env['fit.subscription'].create(
                    {'subscription_partner': partner.id,
                     'subscription_start': subscription_start,
                     'subscription_end': subscription_end,
                     'subscription_type': product.fit_subscription_type,
                     })
            else:
                if subscription_type == 'tickets':
                    self.env['fit.subscription'].create(
                        {'subscription_partner': partner.id,
                         'subscription_counter': subscription_length,
                         'subscription_type': product.fit_subscription_type,
                         })

    def _get_latest_subscription(self, partner):
        latest_end_date = datetime.now().date()
        for subscription in partner.fit_subscriptions:
            if subscription.subscription_type == 'cf_montly' or subscription.subscription_type == 'bc_montly':
                    end_date = datetime.strptime(subscription.subscription_end, '%Y-%m-%d').date()
                    if end_date > latest_end_date:
                        latest_end_date = end_date

        return latest_end_date

    def get_subscription_type_length(self, product, invoice_line):
        given_type = product.fit_subscription_type
        if self.get_subscription_type(given_type) == 'subscription':
            return int(invoice_line.quantity)
        else:
            if self.get_subscription_type(given_type) == 'tickets':
                return int(invoice_line.quantity)*10
        return 0

    def get_subscription_type(self, given_type):
        type_type = {
            'cf_montly': 'subscription',
            'bc_montly': 'subscription',
            'bc_tickets': 'tickets',
            'bz_tickets': 'tickets',
        }
        return type_type.get(given_type, '')