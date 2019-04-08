import logging
from odoo import fields, models, api
_logger = logging.getLogger(__name__)


class Product(models.Model):
    _name = 'product.template'
    _inherit = ['product.template']

    fit_subscription_type = fields.Selection([('ai_montly', 'Maandelijks (All-in)'),
                                          ('cf_montly', 'Maandelijks (Crosstraining)'),
                                          ('bc_montly', 'Maandelijks (Bootcamp)'),
                                          ('bc_tickets', 'Strippenkaart (Bootcamp)'),
                                          ('bz_tickets', 'Strippenkaart (Bokszak)')], string='Type inschrijving')
