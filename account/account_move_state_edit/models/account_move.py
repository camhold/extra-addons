
from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    state = fields.Selection(
        readonly=False
    )
