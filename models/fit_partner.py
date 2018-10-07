import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import fields, models

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner']

    fit_subscriptions = fields.One2many(comodel_name='fit.subscription', inverse_name='subscription_partner', string='Inschrijving',
                                        store='True')

    def can_subscribe(self, event):
        can_subscribe = False
        event_type = str(event.event_type_id.name).lower()
        event_start = datetime.strptime(event.date_begin_located, '%Y-%m-%d %H:%M:%S')
        if event_type == 'open':
            return True
        if event_start < datetime.now():
            return False
        if (event_start + relativedelta(hours=-24)) > datetime.now() and event_type == 'crossfit':
            return False
        for subscription in self.fit_subscriptions:
            if subscription._can_subscribe(event.event_type_id):
                can_subscribe = True
        return can_subscribe

    def can_unsubscribe(self, event):
        event_start = datetime.strptime(event.date_begin_located, '%Y-%m-%d %H:%M:%S')
        if event_start < datetime.now():
            return False
        return True
