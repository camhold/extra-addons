from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    restricted_user = fields.Boolean(string='Restricted User', default=False)
