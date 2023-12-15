from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_medical = fields.Boolean(string='Is Medical')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_medical = fields.Boolean(string='Is Medical', related='product_tmpl_id.is_medical', store=True, readonly=False)
