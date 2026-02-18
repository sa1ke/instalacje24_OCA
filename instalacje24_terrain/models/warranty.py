from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class Instalacje24Warranty(models.Model):
    """Warranty record created automatically after finished jobs."""

    _name = "instalacje24.warranty"
    _description = "Gwarancja"
    _order = "end_date desc"

    name = fields.Char(string="Numer", required=True, default="Nowa")
    active = fields.Boolean(default=True)
    job_id = fields.Many2one("instalacje24.field.job", string="Zlecenie", required=True)
    partner_id = fields.Many2one("res.partner", string="Klient", related="job_id.partner_id", store=True)
    start_date = fields.Date(string="Początek", required=True, default=fields.Date.today)
    end_date = fields.Date(string="Koniec", compute="_compute_end", store=True)
    duration_months = fields.Integer(string="Miesięcy", default=12)
    state = fields.Selection([("active", "Aktywna"), ("expiring", "Kończy się"), ("expired", "Wygasła")], default="active")

    @api.depends("start_date", "duration_months")
    def _compute_end(self):
        for rec in self:
            rec.end_date = rec.start_date + relativedelta(months=rec.duration_months) if rec.start_date else False

    @api.model
    def create(self, vals):
        if vals.get("name", "Nowa") == "Nowa":
            vals["name"] = self.env["ir.sequence"].next_by_code("instalacje24.warranty") or "Nowa"
        return super().create(vals)


    @api.model
    def _cron_mark_expiring(self):
        limit = fields.Date.today() + relativedelta(days=14)
        self.search([("state", "=", "active"), ("end_date", "<=", limit)]).write({"state": "expiring"})
        self.search([("end_date", "<", fields.Date.today())]).write({"state": "expired"})
