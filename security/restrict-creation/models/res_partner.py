from odoo import models, api
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        if self.env['ir.config_parameter'].sudo().get_param('restrict_creation.restrict_contact_creation'):
            if self.env.user.restricted_user:
                raise UserError('La creación de nuevos contactos está restringida para tu usuario.')
        return super(ResPartner, self).create(vals)
