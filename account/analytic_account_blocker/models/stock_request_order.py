from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError


class StockRequestOrder(models.Model):
    _inherit = "stock.request.order"

    analytic_account_ids = fields.Many2many(domain='[("is_blocked", "=", False)]')
