from odoo import fields, models


class Instalacje24ErrorLog(models.Model):
    """Operational log for sync and runtime issues with manual retry tracking."""

    _name = "instalacje24.error.log"
    _description = "Log błędów Instalacje24"
    _order = "create_date desc"

    name = fields.Char(string="Temat", required=True)
    model_name = fields.Char(string="Model")
    record_ref = fields.Char(string="Rekord")
    details = fields.Text(string="Szczegóły")
    state = fields.Selection([("new", "Nowy"), ("retry", "Do ponowienia"), ("done", "Zamknięty")], default="new")
