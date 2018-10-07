import logging
from odoo import fields, models, api
_logger = logging.getLogger(__name__)


class Product(models.Model):
    _name = 'product.template'
    _inherit = ['product.template']

    fit_subscription_type = fields.Selection([('cf_montly', 'Maandelijks (Crossfit)'),
                                          ('cf_quarterly', 'Kwartaal (Crossfit)'),
                                          ('cf_half_year', 'Halfjaar (Crossfit)'),
                                          ('bc_montly', 'Maandelijks (Bootcamp)'),
                                          ('bc_tickets', 'Strippenkaart (Bootcamp)'),
                                          ('bz_tickets', 'Strippenkaart (Bokszak)')], string='Type inschrijving')
