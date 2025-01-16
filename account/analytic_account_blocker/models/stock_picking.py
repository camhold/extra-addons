from odoo import models, fields, _
from odoo.tools import format_date


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    analytic_account_ids = fields.Many2many(domain='[("is_blocked", "=", False)]')
