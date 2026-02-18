from odoo import fields, models


class Instalacje24Complaint(models.Model):
    """Simple complaint flow linked to a field job and customer."""

    _name = "instalacje24.complaint"
    _description = "Reklamacja"
    _order = "create_date desc"

    name = fields.Char(string="Temat", required=True)
    active = fields.Boolean(default=True)
    partner_id = fields.Many2one("res.partner", string="Klient", required=True)
    job_id = fields.Many2one("instalacje24.field.job", string="Zlecenie")
    warranty_id = fields.Many2one("instalacje24.warranty", string="Gwarancja")
    description = fields.Text(string="Opis")
    resolution = fields.Text(string="Rozwiązanie")
    state = fields.Selection([
        ("new", "Nowa"),
        ("in_progress", "W trakcie"),
        ("resolved", "Rozwiązana"),
        ("rejected", "Odrzucona"),
    ], string="Status", default="new")
