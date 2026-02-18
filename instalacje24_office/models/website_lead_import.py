from odoo import fields, models


class Instalacje24WebsiteLeadImport(models.Model):
    """Simple endpoint-like inbox for website leads and manual conversion."""

    _name = "instalacje24.website.lead"
    _description = "Lead z WWW"

    name = fields.Char(string="Temat", required=True)
    client_name = fields.Char(string="Klient")
    phone = fields.Char(string="Telefon")
    address = fields.Char(string="Adres")
    description = fields.Text(string="Opis")
    source = fields.Char(string="Źródło", default="website")
    state = fields.Selection([("new", "Nowy"), ("converted", "Przekształcony")], default="new")

    def action_convert(self):
        for rec in self:
            partner = self.env["res.partner"].create({"name": rec.client_name or rec.name, "phone": rec.phone})
            self.env["instalacje24.lead"].create({
                "name": rec.name,
                "partner_id": partner.id,
                "phone": rec.phone,
                "address": rec.address,
                "description": rec.description,
                "planned_date": fields.Datetime.now(),
            })
            rec.state = "converted"
