from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    restrict_product_creation = fields.Boolean(string='Restrict Product Creation')
    restrict_contact_creation = fields.Boolean(string='Restrict Contact Creation')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('restrict_creation.restrict_product_creation', self.restrict_product_creation)
        self.env['ir.config_parameter'].sudo().set_param('restrict_creation.restrict_contact_creation', self.restrict_contact_creation)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            restrict_product_creation=self.env['ir.config_parameter'].sudo().get_param('restrict_creation.restrict_product_creation', default=False),
            restrict_contact_creation=self.env['ir.config_parameter'].sudo().get_param('restrict_creation.restrict_contact_creation', default=False),
        )
        return res
