from datetime import timedelta
from odoo import api, fields, models


class Instalacje24Dashboard(models.TransientModel):
    """Single-screen KPI dashboard for weekly one-person operations."""

    _name = "instalacje24.dashboard"
    _description = "Dashboard hydraulika"

    revenue_week = fields.Monetary(string="Przychód tydzień", currency_field="currency_id", compute="_compute_values")
    jobs_week = fields.Integer(string="Zlecenia tydzień", compute="_compute_values")
    km_week = fields.Float(string="KM tydzień", compute="_compute_values")
    profit_week = fields.Monetary(string="Zysk tydzień", currency_field="currency_id", compute="_compute_values")
    avg_job_time = fields.Float(string="Śr. czas zlecenia", compute="_compute_values")
    complaints_rate = fields.Float(string="Wskaźnik reklamacji %", compute="_compute_values")
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)

    @api.depends_context("uid")
    def _compute_values(self):
        start = fields.Datetime.now() - timedelta(days=7)
        for rec in self:
            jobs = self.env["instalacje24.field.job"].search([("start_time", ">=", start), ("user_id", "=", self.env.user.id)])
            rec.jobs_week = len(jobs)
            rec.km_week = sum(j.travel_km for j in jobs)
            rec.revenue_week = sum(j.revenue_amount for j in jobs)
            rec.profit_week = sum(j.profit_amount for j in jobs)
            rec.avg_job_time = sum(j.duration for j in jobs) / len(jobs) if jobs else 0.0
            complaints = self.env["instalacje24.complaint"].search_count([("create_date", ">=", start), ("state", "!=", "rejected")])
            rec.complaints_rate = (complaints / rec.jobs_week * 100.0) if rec.jobs_week else 0.0
