# -*- coding: utf-8 -*-
# Copyright 2018 Fundament IT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'FIT BCNL Events Reports',
    'category': 'Website',
    'version': '10.0.0.0.1',
    'author': 'Fundament IT',
    'website': 'https://fundament.it/',
    'licence': 'AGPL-3',
    'depends': ['fit_bcnl_events'],
    'summary':"""
Fundament IT (FIT) BCNL Events reports.
""",
    'description': """
Reports for the BCNL app; for example partner subscriptions.
    """,
    'data': [
        'report/fit_report_subscription_view.xml',
    ],
    'installable': True,
}