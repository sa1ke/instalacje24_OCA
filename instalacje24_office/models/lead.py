from odoo import api, fields, models, _
from odoo.exceptions import UserError


class Instalacje24Lead(models.Model):
    """Lightweight CRM lead dedicated to one-person plumbing workflows."""

    _name = "instalacje24.lead"
    _description = "Lead hydraulika"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "planned_date desc, id desc"

    name = fields.Char(string="Temat", required=True, tracking=True)
    partner_id = fields.Many2one("res.partner", string="Klient", tracking=True)
    user_id = fields.Many2one("res.users", string="Przypisany", default=lambda self: self.env.user, required=True)
    phone = fields.Char(string="Telefon")
    address = fields.Char(string="Adres")
    problem_type = fields.Selection([
        ("boiler", "Kocioł"),
        ("leak", "Wyciek"),
        ("installation", "Nowa instalacja"),
        ("maintenance", "Przegląd"),
        ("other", "Inne"),
    ], string="Typ problemu", default="other", required=True)
    description = fields.Text(string="Opis")
    photo_ids = fields.Many2many("ir.attachment", string="Zdjęcia")
    planned_date = fields.Datetime(string="Planowany termin", required=True, default=fields.Datetime.now)
    status = fields.Selection([
        ("new", "Nowy"),
        ("quoted", "Wycena"),
        ("planned", "Zaplanowany"),
        ("done", "Zakończony"),
        ("cancelled", "Anulowany"),
    ], string="Status", default="new", tracking=True)
    terrain_job_id = fields.Many2one("instalacje24.field.job", string="Zlecenie terenowe")
    quote_id = fields.Many2one("instalacje24.quote", string="Wycena")
    sale_order_id = fields.Many2one("sale.order", string="Zamówienie")

    def action_create_terrain_job(self):
        self.ensure_one()
        if self.terrain_job_id:
            return self.terrain_job_id.get_formview_action()
        partner = self.partner_id
        if not partner and self.phone:
            partner = self.env["res.partner"].create({"name": self.name, "phone": self.phone})
        job = self.env["instalacje24.field.job"].create({
            "name": self.name,
            "partner_id": partner.id,
            "phone": self.phone,
            "address": self.address,
            "description": self.description,
            "planned_start": self.planned_date,
            "user_id": self.user_id.id,
        })
        self.write({"terrain_job_id": job.id, "status": "planned"})
        return job.get_formview_action()

    def action_mark_done(self):
        for lead in self:
            lead.status = "done"
            if lead.terrain_job_id and not lead.terrain_job_id.invoice_id:
                lead.terrain_job_id.action_create_invoice()


    def action_view_customer_history(self):
        self.ensure_one()
        if not self.partner_id:
            return False
        return {
            "type": "ir.actions.act_window",
            "name": _("Historia klienta"),
            "res_model": "instalacje24.field.job",
            "view_mode": "tree,form",
            "domain": [("partner_id", "=", self.partner_id.id)],
        }

    def action_open_calendar(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Kalendarz zleceń"),
            "res_model": "instalacje24.lead",
            "view_mode": "calendar,tree,form",
            "context": {"default_user_id": self.env.user.id},
        }

    @api.constrains("terrain_job_id", "status")
    def _check_done_has_job(self):
        for lead in self:
            if lead.status == "done" and not lead.terrain_job_id:
                raise UserError(_("Status zakończony wymaga powiązanego zlecenia terenowego."))
