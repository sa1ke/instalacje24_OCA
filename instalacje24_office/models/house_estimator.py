from odoo import api, fields, models


class Instalacje24HouseEstimator(models.Model):
    """Rule-based estimator for larger house plumbing installations."""

    _name = "instalacje24.house.estimator"
    _description = "Estimator instalacji domu"

    name = fields.Char(string="Nazwa", required=True, default="Nowa kalkulacja")
    partner_id = fields.Many2one("res.partner", string="Klient")
    house_size_m2 = fields.Float(string="Powierzchnia m²", required=True)
    bathrooms_count = fields.Integer(string="Liczba łazienek", default=1)
    floors_count = fields.Integer(string="Liczba kondygnacji", default=1)
    heating_type = fields.Selection([("gas", "Gaz"), ("pump", "Pompa ciepła"), ("electric", "Elektryczne")], default="gas", string="Ogrzewanie")
    installation_type = fields.Selection([("new", "Nowa"), ("modernization", "Modernizacja")], default="new", string="Typ instalacji")
    quality_level = fields.Selection([("budget", "Budżet"), ("standard", "Standard"), ("premium", "Premium")], default="standard", string="Poziom jakości")
    estimated_material_cost = fields.Float(string="Szacowany koszt materiałów", compute="_compute_estimate", store=True)
    estimated_labor_hours = fields.Float(string="Szacowany czas pracy", compute="_compute_estimate", store=True)
    estimated_total_price = fields.Float(string="Cena szacowana", compute="_compute_estimate", store=True)
    price_range_min = fields.Float(string="Przedział min", compute="_compute_estimate", store=True)
    price_range_max = fields.Float(string="Przedział max", compute="_compute_estimate", store=True)

    @api.depends("house_size_m2", "bathrooms_count", "floors_count", "heating_type", "installation_type", "quality_level")
    def _compute_estimate(self):
        params = self.env["ir.config_parameter"].sudo()
        base_m2 = float(params.get_param("instalacje24_office.estimator_base_m2", default="180"))
        bath_factor = float(params.get_param("instalacje24_office.estimator_bathroom_factor", default="2500"))
        floor_factor = float(params.get_param("instalacje24_office.estimator_floor_factor", default="1800"))
        labor_per_m2 = float(params.get_param("instalacje24_office.estimator_labor_per_m2", default="0.12"))
        quality = {"budget": 0.9, "standard": 1.0, "premium": 1.25}
        heat = {"gas": 1.0, "pump": 1.3, "electric": 0.85}
        inst = {"new": 1.0, "modernization": 0.8}
        for rec in self:
            multiplier = quality.get(rec.quality_level, 1.0) * heat.get(rec.heating_type, 1.0) * inst.get(rec.installation_type, 1.0)
            rec.estimated_material_cost = (rec.house_size_m2 * base_m2 + rec.bathrooms_count * bath_factor + rec.floors_count * floor_factor) * multiplier
            rec.estimated_labor_hours = rec.house_size_m2 * labor_per_m2 * multiplier
            rec.estimated_total_price = rec.estimated_material_cost + (rec.estimated_labor_hours * 180)
            rec.price_range_min = rec.estimated_total_price * 0.9
            rec.price_range_max = rec.estimated_total_price * 1.15

    def action_create_quote(self):
        self.ensure_one()
        lead = self.env["instalacje24.lead"].create({
            "name": self.name,
            "partner_id": self.partner_id.id,
            "planned_date": fields.Datetime.now(),
            "problem_type": "installation",
        })
        quote = self.env["instalacje24.quote"].create({
            "lead_id": lead.id,
            "service_type": "installation",
            "labor_hours": self.estimated_labor_hours,
            "hourly_rate": 180,
            "material_cost": self.estimated_material_cost,
            "travel_km": 0,
        })
        return quote.get_formview_action()
