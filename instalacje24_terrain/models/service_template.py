from odoo import fields, models


class Instalacje24ServiceTemplate(models.Model):
    """Reusable plumbing service template with pricing and default materials."""

    _name = "instalacje24.service.template"
    _description = "Szablon usługi hydraulicznej"

    name = fields.Char(string="Nazwa", required=True)
    active = fields.Boolean(default=True)
    fixed_price = fields.Float(string="Cena ryczałtowa")
    default_hours = fields.Float(string="Domyślne godziny", default=1.0)
    material_line_ids = fields.One2many("instalacje24.service.template.material", "template_id", string="Materiały domyślne")


class Instalacje24ServiceTemplateMaterial(models.Model):
    """Default material list tied to a service template."""

    _name = "instalacje24.service.template.material"
    _description = "Materiał szablonu usługi"

    template_id = fields.Many2one("instalacje24.service.template", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Produkt", required=True)
    quantity = fields.Float(string="Ilość", default=1.0)
