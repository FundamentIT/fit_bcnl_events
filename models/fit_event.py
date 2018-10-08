import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class FitEvent(models.Model):
    _name = 'event.event'
    _inherit = ['event.event']

    website_published = fields.Boolean(default=True)
    fit_day_of_week = fields.Char(string='Dag', default='')
    fit_repetition_enabled = fields.Boolean(string='Herhalen?', default=False)
    fit_repetition = fields.Selection([('daily', 'Dagelijks'),
                                       ('weekly', 'Wekelijks'),
                                       ('monthly', 'Maandelijks')], string="Schema herhaling")

    @api.onchange('date_begin')
    def update_day_of_week(self):
        start_date = self.date_begin_located
        if start_date:
            self.fit_day_of_week = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').strftime('%a')

    def start_automatic_event_creation(self):
        repeating_event_ids = self.env['event.event'].search([('fit_repetition_enabled', '=', True)])
        for repeating_event in repeating_event_ids:
            _logger.info('Found repeating event: ' + repeating_event.name)
            if repeating_event.fit_repetition == 'daily':
                self._handle_daily_event_repetition(repeating_event)
            if repeating_event.fit_repetition == 'weekly':
                self._handle_weekly_event_repetition(repeating_event)
            if repeating_event.fit_repetition == 'monthly':
                self._handle_montly_event_repetition(repeating_event)

    def _handle_daily_event_repetition(self, old_repeating_event):
        _logger.info('Handling daily repeating event')
        end_date = datetime.strptime(old_repeating_event.date_end, '%Y-%m-%d %H:%M:00')
        present = datetime.now()
        if present >= end_date:
            new_start_date = datetime.strptime(old_repeating_event.date_begin, '%Y-%m-%d %H:%M:00') + relativedelta(days=+1)
            new_end_date = end_date + relativedelta(days=+1)
            if self._event_does_not_exist(old_repeating_event, new_end_date):
                self._create_new_event(old_repeating_event, new_start_date, new_end_date)

    def _handle_weekly_event_repetition(self, old_repeating_event):
        _logger.info('Handling weekly repeating event')
        end_date = datetime.strptime(old_repeating_event.date_end, '%Y-%m-%d %H:%M:00')
        present = datetime.now()
        if present >= end_date:
            new_start_date = datetime.strptime(old_repeating_event.date_begin, '%Y-%m-%d %H:%M:00') + relativedelta(days=+7)
            new_end_date = end_date + relativedelta(days=+7)
            if self._event_does_not_exist(old_repeating_event, new_end_date):
                self._create_new_event(old_repeating_event, new_start_date, new_end_date)

    def _handle_monthly_event_repetition(self, old_repeating_event):
        _logger.info('Handling monthly repeating event')
        end_date = datetime.strptime(old_repeating_event.date_end, '%Y-%m-%d %H:%M:00')
        present = datetime.now()
        if present >= end_date:
            new_start_date = datetime.strptime(old_repeating_event.date_begin, '%Y-%m-%d %H:%M:00') + relativedelta(months=+1)
            new_end_date = end_date + relativedelta(months=+1)
            if self._event_does_not_exist(old_repeating_event, new_end_date):
                self._create_new_event(old_repeating_event, new_start_date, new_end_date)

    def _event_does_not_exist(self, old_repeating_event, new_end_date):
        _logger.info('Checking new event exisitence: ' + old_repeating_event.name + ', date: ' + str(new_end_date))
        old_event_cat = old_repeating_event.event_type_id.id
        existing_event = self.env['event.event'].search([('event_type_id', '=', old_event_cat), ('date_end', '=', str(new_end_date))])
        if existing_event:
            return False
        else:
            return True

    def _create_new_event(self, old_repeating_event, new_start_date, new_end_date):
        _logger.info('Start creation new repeating event')
        new_repeating_event = old_repeating_event.copy(default={'website_published': True})
        new_repeating_event.date_end = new_end_date
        new_repeating_event.date_begin=new_start_date

        # 'date_begin': str(new_start_date), 'date_end_': str(new_end_date),
        old_repeating_event.fit_repetition_enabled = False
        old_repeating_event.fit_repetition = ''
