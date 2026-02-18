from odoo import fields, models


class Instalacje24QuickJobWizard(models.TransientModel):
    """Very fast office wizard to create a lead and terrain job in one flow."""

    _name = "instalacje24.quick.job.wizard"
    _description = "Szybkie nowe zlecenie"

    partner_id = fields.Many2one("res.partner", string="Klient", required=True)
    phone = fields.Char(string="Telefon")
    address = fields.Char(string="Adres", required=True)
    description = fields.Text(string="Opis")
    planned_date = fields.Datetime(string="Termin", required=True, default=fields.Datetime.now)

    def action_create(self):
        self.ensure_one()
        lead = self.env["instalacje24.lead"].create({
            "name": f"{self.partner_id.display_name} - szybkie zlecenie",
            "partner_id": self.partner_id.id,
            "phone": self.phone or self.partner_id.phone,
            "address": self.address,
            "description": self.description,
            "planned_date": self.planned_date,
            "user_id": self.env.user.id,
        })
        return lead.action_create_terrain_job()
