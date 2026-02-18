from odoo import fields, models


class Instalacje24VanInventory(models.Model):
    """Simple mini-van inventory to track stock carried by a single plumber."""

    _name = "instalacje24.van.inventory"
    _description = "Magazyn busa"

    product_id = fields.Many2one("product.product", string="Produkt", required=True)
    quantity = fields.Float(string="Ilość w busie", default=0.0)
    min_quantity = fields.Float(string="Stan minimalny", default=1.0)
    note = fields.Char(string="Notatka")
