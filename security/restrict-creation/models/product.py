from odoo import models, api
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        if self.env['ir.config_parameter'].sudo().get_param('restrict_creation.restrict_product_creation'):
            if self.env.user.restricted_user:
                raise UserError('La creación de nuevos productos está restringida para tu usuario.')
        return super(ProductTemplate, self).create(vals)
