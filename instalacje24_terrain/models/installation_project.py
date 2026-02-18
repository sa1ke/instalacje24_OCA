from odoo import api, fields, models


class Instalacje24InstallationProject(models.Model):
    """Light project mode for larger plumbing installation jobs."""

    _name = "instalacje24.installation.project"
    _description = "Projekt instalacji"

    name = fields.Char(string="Nazwa", required=True)
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one("res.partner", string="Klient", required=True)
    start_date = fields.Date(string="Start")
    end_date = fields.Date(string="Koniec")
    stage = fields.Selection([
        ("analysis", "Analiza"),
        ("offer", "Oferta"),
        ("materials", "Materiały"),
        ("execution", "Realizacja"),
        ("handover", "Odbiór"),
        ("done", "Zamknięty"),
    ], default="analysis", string="Etap")
    checklist = fields.Text(string="Checklista")
    material_plan_ids = fields.One2many("instalacje24.installation.project.material", "project_id", string="Plan materiałów")
    budget_amount = fields.Monetary(string="Budżet", currency_field="currency_id")
    real_cost_amount = fields.Monetary(string="Koszt rzeczywisty", compute="_compute_cost", currency_field="currency_id", store=True)
    margin_amount = fields.Monetary(string="Różnica", compute="_compute_cost", currency_field="currency_id", store=True)
    drawing_ids = fields.Many2many("ir.attachment", string="Rysunki i zdjęcia")
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)

    @api.depends("material_plan_ids.quantity", "material_plan_ids.purchase_price", "budget_amount")
    def _compute_cost(self):
        for rec in self:
            rec.real_cost_amount = sum(line.quantity * line.purchase_price for line in rec.material_plan_ids)
            rec.margin_amount = rec.budget_amount - rec.real_cost_amount


class Instalacje24InstallationProjectMaterial(models.Model):
    """Material planning lines for installation project mode."""

    _name = "instalacje24.installation.project.material"
    _description = "Materiał projektu instalacji"

    project_id = fields.Many2one("instalacje24.installation.project", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Produkt", required=True)
    quantity = fields.Float(string="Ilość", default=1.0)
    purchase_price = fields.Float(string="Cena zakupu")
