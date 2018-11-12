# -*- coding: utf-8 -*-

from odoo import api, models, fields, tools


class FitReportSubscription(models.Model):
    """Subscription Analysis"""
    _name = "fit.report.subscription"
    _order = 'start desc'
    _auto = False

    id = fields.Char('ID', readonly=True)
    partner_name = fields.Char('Deelnemer', readonly=True)

    create_date = fields.Date('Inschrijving aangemaakt', readonly=True)
    write_date = fields.Date('Inschrijving bijgewerkt', readonly=True)
    start = fields.Date('Inschrijving Start', readonly=True)
    end = fields.Date('Inschrijving Einde', readonly=True)
    counter = fields.Char('# Tickets', readonly=True)
    type = fields.Selection([('cf_montly', 'Maandelijks (Crossfit)'),
                                          ('bc_montly', 'Maandelijks (Bootcamp)'),
                                          ('bc_tickets', 'Strippenkaart (Bootcamp)'),
                                          ('bz_tickets', 'Strippenkaart (Bokszak)')],'Type', readonly=True, required=True)

    due_time_week = fields.Integer(' # Verloopt binnen een week')
    due_time_day = fields.Integer(' # Verloopt binnen een dag')
    subscription_state = fields.Selection([('due_other', 'Langdurig'), ('due_time_week', 'Binnen een week'),
                                           ('due_time_day', 'Binnen een dag'), ('due_ticket_one','1 ticket'),
                                           ('due_ticket_five', '< 5 tickets')],
                                        'Abonnement Status', readonly=True, required=True)
    subscription_update = fields.Selection([('update_week', 'Deze week'), ('update_month', 'Deze maand'),('update_other', 'Langer geleden')])

    def _select(self):
        return """
            SELECT
                p.name AS id,
                date(s.create_date) as create_date,
                date(s.write_date) as write_date,
                date(s.subscription_start) as start,
                date(s.subscription_end) as end,
                s.subscription_counter as counter,
                s.subscription_type as type,
                p.name as partner_name,
                CASE 
                    WHEN (s.write_date >= (date(now()) - integer '0')) THEN 'update_today' 
                    WHEN (s.write_date >= (date(now()) - integer '7')) THEN 'update_week' 
                    WHEN (s.write_date >= date_trunc('day', current_date - interval '1' month)) THEN 'update_month' 
                    ELSE 'update_other' 
                END AS subscription_update,
                CASE 
                    WHEN (subscription_end >= now() and subscription_end <= (date(now()) + integer '1')) THEN 'due_time_day' 
                    WHEN (subscription_end >= now() and subscription_end <= (date(now()) + integer '7')) THEN 'due_time_week'
                    WHEN subscription_counter = 1 THEN 'due_ticket_one' 
                    WHEN subscription_counter <= 5 THEN 'due_ticket_five' 
                    ELSE 'due_other'
                END AS subscription_state,
                CASE WHEN (subscription_end >= now() and subscription_end <= (date(now()) + integer '7')) THEN count(s.id) ELSE 0 END AS due_time_week,
                CASE WHEN (subscription_end >= now() and subscription_end <= (date(now()) + integer '1')) THEN count(s.id) ELSE 0 END AS due_time_day
            """

    def _from(self):
        return """
            FROM
                fit_subscription s
                LEFT JOIN res_partner p ON (s.subscription_partner=p.id)
            """

    def _group_by(self):
        return """
            GROUP BY
                p.name,
                s.id
            """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            "CREATE or REPLACE VIEW %s as (%s %s %s)" % (
                self._table, self._select(), self._from(), self._group_by(),
            )
        )
