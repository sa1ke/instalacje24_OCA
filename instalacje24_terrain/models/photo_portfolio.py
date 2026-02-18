from odoo import fields, models


class Instalacje24PhotoPortfolio(models.Model):
    """Before/after photo portfolio for showcasing completed plumbing jobs."""

    _name = "instalacje24.photo.portfolio"
    _description = "Portfolio zdjęć"
    _order = "create_date desc"

    name = fields.Char(string="Tytuł", required=True)
    job_id = fields.Many2one("instalacje24.field.job", string="Zlecenie")
    partner_id = fields.Many2one("res.partner", string="Klient")
    image_before = fields.Image(string="Zdjęcie przed")
    image_after = fields.Image(string="Zdjęcie po")
    note = fields.Text(string="Opis")
