from odoo import api, fields, models
from odoo.exceptions import UserError


class Instalacje24Quote(models.Model):
    """Plumbing quote calculator with cost, margin and quick-price helpers."""

    _name = "instalacje24.quote"
    _description = "Kalkulator wyceny"

    name = fields.Char(string="Numer", default="Nowa", copy=False)
    lead_id = fields.Many2one("instalacje24.lead", string="Lead", required=True)
    service_type = fields.Selection([
        ("quick", "Szybka naprawa"),
        ("boiler", "Serwis kotła"),
        ("installation", "Montaż instalacji"),
    ], string="Usługa", required=True)
    labor_hours = fields.Float(string="Roboczogodziny", default=1.0)
    hourly_rate = fields.Float(string="Stawka/h", default=lambda self: self._get_default_rate("hourly_rate"))
    material_cost = fields.Float(string="Koszt materiałów", default=0.0)
    travel_km = fields.Float(string="Dojazd km", default=0.0)
    travel_rate = fields.Float(string="Stawka/km", default=lambda self: self._get_default_rate("travel_rate"))
    margin_percent = fields.Float(string="Marża %", default=lambda self: self._get_default_rate("margin_percent"))
    vat_percent = fields.Float(string="VAT %", default=lambda self: self._get_default_rate("vat_percent"))
    total_net = fields.Float(string="Razem netto", compute="_compute_totals", store=True)
    total_gross = fields.Float(string="Razem brutto", compute="_compute_totals", store=True)
    sale_order_id = fields.Many2one("sale.order", string="Zamówienie")

    @api.model
    def create(self, vals):
        if vals.get("name", "Nowa") == "Nowa":
            vals["name"] = self.env["ir.sequence"].next_by_code("instalacje24.quote") or "Nowa"
        return super().create(vals)

    @api.model
    def _get_default_rate(self, key):
        params = self.env["ir.config_parameter"].sudo()
        return float(params.get_param(f"instalacje24_office.{key}", default="0"))

    @api.depends("labor_hours", "hourly_rate", "material_cost", "travel_km", "travel_rate", "margin_percent", "vat_percent")
    def _compute_totals(self):
        for rec in self:
            base = rec.labor_hours * rec.hourly_rate + rec.material_cost + rec.travel_km * rec.travel_rate
            net = base * (1.0 + (rec.margin_percent / 100.0))
            rec.total_net = net
            rec.total_gross = net * (1.0 + (rec.vat_percent / 100.0))

    def action_generate_quote(self):
        self.ensure_one()
        if not self.lead_id.partner_id:
            raise UserError("Lead musi mieć klienta, aby utworzyć ofertę.")
        order = self.env["sale.order"].create({
            "partner_id": self.lead_id.partner_id.id,
            "origin": self.name,
            "note": self.lead_id.description,
            "order_line": [(0, 0, {"name": self._service_label(), "product_uom_qty": 1, "price_unit": self.total_net})],
        })
        self.sale_order_id = order.id
        self.lead_id.write({"sale_order_id": order.id, "status": "quoted", "quote_id": self.id})
        return order.get_formview_action()

    def action_set_quick_repair(self):
        self._apply_quick_price("instalacje24_office.quick_price_repair", "quick")

    def action_set_boiler_service(self):
        self._apply_quick_price("instalacje24_office.quick_price_boiler", "boiler")

    def action_set_installation(self):
        self._apply_quick_price("instalacje24_office.quick_price_installation", "installation")

    def _apply_quick_price(self, key, service_type):
        for rec in self:
            price = float(self.env["ir.config_parameter"].sudo().get_param(key, default="0"))
            rec.update({"service_type": service_type, "labor_hours": 1.0, "material_cost": 0.0, "travel_km": 0.0, "hourly_rate": price or rec.hourly_rate})

    def _service_label(self):
        labels = dict(self._fields["service_type"].selection)
        return labels.get(self.service_type, "Usługa hydrauliczna")

    def action_print_offer_pdf(self):
        self.ensure_one()
        return self.env.ref("sale.action_report_saleorder").report_action(self.sale_order_id) if self.sale_order_id else False
