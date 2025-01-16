from odoo import api, exceptions, models
from odoo.tools import Query


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        res = super(BaseModel, self).name_search(name, args, operator, limit)
        res_resp = res.copy()
        if res:
            for item in res:
                if len(item) >= 2 and self._table == 'account_analytic_account':
                    analytic_account_id = self.env['account.analytic.account'].search([('id', '=', item[0])])
                    if not analytic_account_id:
                        res_resp = tuple(item_res for item_res in res_resp if item_res[0] != item[0])
        return res_resp

