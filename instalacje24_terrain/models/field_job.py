from datetime import timedelta
from odoo import api, fields, models, _


class Instalacje24FieldJob(models.Model):
    """Tablet-first field service order with timing, photos, signature and invoicing."""

    _name = "instalacje24.field.job"
    _description = "Zlecenie terenowe hydraulika"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "planned_start desc, id desc"

    name = fields.Char(string="Temat", required=True, default="Nowe zlecenie")
    active = fields.Boolean(default=True)
    user_id = fields.Many2one("res.users", string="Hydraulik", default=lambda self: self.env.user, required=True)
    partner_id = fields.Many2one("res.partner", string="Klient", required=True)
    phone = fields.Char(string="Telefon")
    address = fields.Char(string="Adres", required=True)
    google_maps_url = fields.Char(string="Google Maps", compute="_compute_google_maps_url")
    route_url = fields.Char(string="Trasa", compute="_compute_route_url")
    whatsapp_url = fields.Char(string="WhatsApp", compute="_compute_whatsapp_url")
    description = fields.Text(string="Opis")
    service_template_id = fields.Many2one("instalacje24.service.template", string="Szablon usługi")
    planned_start = fields.Datetime(string="Planowany start")
    start_time = fields.Datetime(string="Start")
    end_time = fields.Datetime(string="Stop")
    duration = fields.Float(string="Czas (h)", compute="_compute_duration", store=True)
    material_line_ids = fields.One2many("instalacje24.field.material", "job_id", string="Materiały")
    materials_used = fields.Text(string="Materiały użyte", compute="_compute_materials_used")
    notes = fields.Text(string="Notatki")
    voice_note_placeholder = fields.Char(string="Voice-to-text", default="TODO: integracja voice-to-text")
    photos_before = fields.Many2many("ir.attachment", "inst24_job_photo_before_rel", "job_id", "attachment_id", string="Zdjęcia przed")
    photos_after = fields.Many2many("ir.attachment", "inst24_job_photo_after_rel", "job_id", "attachment_id", string="Zdjęcia po")
    customer_signature = fields.Image(string="Podpis klienta", max_width=1280, max_height=1280)
    payment_status = fields.Selection([
        ("not_paid", "Nieopłacone"),
        ("partial", "Częściowo opłacone"),
        ("paid", "Opłacone"),
    ], string="Płatność", default="not_paid", tracking=True)
    state = fields.Selection([
        ("draft", "Nowe"),
        ("in_progress", "W trakcie"),
        ("done", "Zakończone"),
    ], string="Status", default="draft", tracking=True)
    sale_order_id = fields.Many2one("sale.order", string="Zamówienie")
    invoice_id = fields.Many2one("account.move", string="Faktura")
    travel_km = fields.Float(string="Dojazd km")
    revenue_amount = fields.Monetary(string="Przychód", compute="_compute_financials", currency_field="currency_id", store=True)
    cost_amount = fields.Monetary(string="Koszt", compute="_compute_financials", currency_field="currency_id", store=True)
    profit_amount = fields.Monetary(string="Zysk", compute="_compute_financials", currency_field="currency_id", store=True)
    margin_percent = fields.Float(string="Marża %", compute="_compute_financials", store=True)
    margin_alert = fields.Boolean(string="Alert marży", compute="_compute_financials", store=True)
    done_date = fields.Date(string="Data zakończenia", readonly=True)
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)
    recurring = fields.Boolean(string="Cykliczne")
    recurring_interval_months = fields.Integer(string="Interwał mies.", default=12)
    next_recurring_date = fields.Date(string="Następna data")

    @api.depends("address")
    def _compute_google_maps_url(self):
        for rec in self:
            rec.google_maps_url = f"https://www.google.com/maps/search/?api=1&query={rec.address or ''}"

    @api.depends("address")
    def _compute_route_url(self):
        for rec in self:
            rec.route_url = f"https://www.google.com/maps/dir/?api=1&destination={rec.address or ''}"

    @api.depends("phone")
    def _compute_whatsapp_url(self):
        for rec in self:
            phone = (rec.phone or "").replace(" ", "")
            rec.whatsapp_url = f"https://wa.me/{phone}" if phone else False

    @api.depends("start_time", "end_time")
    def _compute_duration(self):
        for rec in self:
            rec.duration = (rec.end_time - rec.start_time).total_seconds() / 3600.0 if rec.start_time and rec.end_time else 0.0

    @api.depends("material_line_ids", "material_line_ids.product_id", "material_line_ids.quantity")
    def _compute_materials_used(self):
        for rec in self:
            rec.materials_used = ", ".join(f"{line.product_id.display_name} x{line.quantity:g}" for line in rec.material_line_ids)

    @api.depends("material_line_ids.quantity", "material_line_ids.product_id", "sale_order_id.amount_total")
    def _compute_financials(self):
        min_margin = float(self.env["ir.config_parameter"].sudo().get_param("instalacje24_terrain.min_margin_percent", default="15"))
        for rec in self:
            material_cost = sum(line.quantity * line.purchase_price for line in rec.material_line_ids)
            rec.cost_amount = material_cost
            rec.revenue_amount = rec.sale_order_id.amount_total if rec.sale_order_id else 0.0
            rec.profit_amount = rec.revenue_amount - rec.cost_amount
            rec.margin_percent = (rec.profit_amount / rec.revenue_amount * 100.0) if rec.revenue_amount else 0.0
            rec.margin_alert = bool(rec.revenue_amount and rec.margin_percent < min_margin)

    @api.onchange("service_template_id")
    def _onchange_service_template_id(self):
        for rec in self:
            if not rec.service_template_id:
                continue
            rec.name = rec.service_template_id.name
            rec.material_line_ids = [(5, 0, 0)] + [
                (0, 0, {
                    "product_id": line.product_id.id,
                    "quantity": line.quantity,
                })
                for line in rec.service_template_id.material_line_ids
            ]

    def action_start_work(self):
        for rec in self:
            rec.write({"start_time": fields.Datetime.now(), "state": "in_progress"})

    def action_stop_work(self):
        for rec in self:
            rec.write({"end_time": fields.Datetime.now()})

    def action_open_maps(self):
        self.ensure_one()
        return {"type": "ir.actions.act_url", "url": self.google_maps_url, "target": "new"}

    def action_open_route(self):
        self.ensure_one()
        return {"type": "ir.actions.act_url", "url": self.route_url, "target": "new"}

    def action_send_on_my_way(self):
        self.ensure_one()
        if self.whatsapp_url:
            return {"type": "ir.actions.act_url", "url": f"{self.whatsapp_url}?text=Jadę%20do%20Pani/Pana.", "target": "new"}
        return True

    def action_send_finished(self):
        self.ensure_one()
        if self.whatsapp_url:
            return {"type": "ir.actions.act_url", "url": f"{self.whatsapp_url}?text=Praca%20zakończona.%20Dziękuję.", "target": "new"}
        return True

    def action_duplicate_previous_for_partner(self):
        self.ensure_one()
        previous = self.search([("partner_id", "=", self.partner_id.id), ("id", "!=", self.id)], order="planned_start desc,id desc", limit=1)
        if not previous:
            return False
        copy = previous.copy({"state": "draft", "start_time": False, "end_time": False, "invoice_id": False, "sale_order_id": False})
        return copy.get_formview_action()

    def action_mark_done(self):
        for rec in self:
            rec.state = "done"
            rec.done_date = fields.Date.today()
            if not rec.invoice_id:
                rec.action_create_invoice()
            if not self.env["instalacje24.warranty"].search_count([("job_id", "=", rec.id)]):
                self.env["instalacje24.warranty"].create({"job_id": rec.id, "start_date": fields.Date.today()})

    def action_soft_delete(self):
        self.write({"active": False})

    def action_restore(self):
        self.write({"active": True})

    def action_create_invoice(self):
        action = True
        for rec in self:
            if rec.invoice_id:
                action = rec.invoice_id.get_formview_action()
                continue
            if not rec.sale_order_id:
                service_price = rec.service_template_id.fixed_price or max(rec.cost_amount * 1.3, 1.0)
                order = self.env["sale.order"].create({
                    "partner_id": rec.partner_id.id,
                    "origin": rec.name,
                    "order_line": [(0, 0, {"name": rec.name or _("Usługa hydrauliczna"), "product_uom_qty": 1, "price_unit": service_price})],
                })
                for line in rec.material_line_ids:
                    order.write({"order_line": [(0, 0, {"product_id": line.product_id.id, "product_uom_qty": line.quantity, "price_unit": line.product_id.lst_price, "name": line.product_id.display_name})]})
                order.action_confirm()
                rec.sale_order_id = order
            invoice = rec.sale_order_id._create_invoices()[:1]
            if invoice:
                rec.invoice_id = invoice
                action = rec.invoice_id.get_formview_action()
        return action

    @api.model
    def _cron_generate_recurring_jobs(self):
        today = fields.Date.today()
        templates = self.search([("recurring", "=", True), ("next_recurring_date", "<=", today), ("state", "=", "done")])
        for template in templates:
            new_job = template.copy({"state": "draft", "start_time": False, "end_time": False, "invoice_id": False, "sale_order_id": False, "planned_start": fields.Datetime.now()})
            template.next_recurring_date = fields.Date.add(today, months=template.recurring_interval_months)
            new_job.message_post(body=_("Automatycznie utworzono zlecenie cykliczne."))

    @api.model
    def _cron_visit_reminder_24h(self):
        now = fields.Datetime.now()
        in_24h = now + timedelta(hours=24)
        jobs = self.search([("state", "in", ["draft", "in_progress"]), ("planned_start", ">=", now), ("planned_start", "<=", in_24h)])
        activity_type = self.env.ref("mail.mail_activity_data_todo")
        model_id = self.env["ir.model"]._get_id("instalacje24.field.job")
        for job in jobs:
            self.env["mail.activity"].create({"res_id": job.id, "res_model_id": model_id, "activity_type_id": activity_type.id, "summary": "Przypomnienie: wizyta za 24h", "user_id": job.user_id.id})

    @api.model
    def _cron_unpaid_7d_reminder(self):
        threshold = fields.Date.today() - timedelta(days=7)
        jobs = self.search([("state", "=", "done"), ("payment_status", "!=", "paid"), ("done_date", "<=", threshold)])
        activity_type = self.env.ref("mail.mail_activity_data_todo")
        model_id = self.env["ir.model"]._get_id("instalacje24.field.job")
        for job in jobs:
            self.env["mail.activity"].create({"res_id": job.id, "res_model_id": model_id, "activity_type_id": activity_type.id, "summary": "Przypomnienie: płatność po 7 dniach", "user_id": job.user_id.id})
