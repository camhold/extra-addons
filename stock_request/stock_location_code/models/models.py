from odoo import models, fields, api
from odoo.exceptions import ValidationError

class StockLocation(models.Model):
    _inherit = 'stock.location'

    code = fields.Char(string='Location Code', required=True, copy=False)

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'The location code must be unique.')
    ]

    @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            if self.search_count([('code', '=', record.code)]) > 1:
                raise ValidationError('The location code must be unique.')
