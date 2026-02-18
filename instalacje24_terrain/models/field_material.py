from odoo import api, fields, models


class Instalacje24FieldMaterial(models.Model):
    """Material line used inside a field job to track consumed products and costs."""

    _name = "instalacje24.field.material"
    _description = "Materiał użyty w zleceniu"

    job_id = fields.Many2one("instalacje24.field.job", string="Zlecenie", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Produkt", required=True)
    quantity = fields.Float(string="Ilość", default=1.0, required=True)
    purchase_price = fields.Float(string="Cena zakupu", default=lambda self: self.product_id.standard_price if self.product_id else 0.0)
    sale_price = fields.Float(string="Cena sprzedaży", related="product_id.lst_price", readonly=True)
    line_cost = fields.Float(string="Koszt", compute="_compute_line_values", store=True)

    @api.depends("quantity", "purchase_price")
    def _compute_line_values(self):
        for rec in self:
            rec.line_cost = rec.quantity * rec.purchase_price
