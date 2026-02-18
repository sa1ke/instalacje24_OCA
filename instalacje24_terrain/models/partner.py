from odoo import fields, models


class ResPartner(models.Model):
    """Partner extension for visit history, warranties, complaints and seasonal reminders."""

    _inherit = "res.partner"

    field_job_count = fields.Integer(string="Liczba wizyt", compute="_compute_counts")
    warranty_count = fields.Integer(string="Gwarancje", compute="_compute_counts")
    complaint_count = fields.Integer(string="Reklamacje", compute="_compute_counts")
    seasonal_reminder = fields.Boolean(string="Przypomnienie sezonowe")
    seasonal_reminder_month = fields.Selection([(str(i), str(i)) for i in range(1, 13)], string="Miesiąc przypomnienia")

    def _compute_counts(self):
        for partner in self:
            partner.field_job_count = self.env["instalacje24.field.job"].search_count([("partner_id", "=", partner.id)])
            partner.warranty_count = self.env["instalacje24.warranty"].search_count([("partner_id", "=", partner.id)])
            partner.complaint_count = self.env["instalacje24.complaint"].search_count([("partner_id", "=", partner.id)])

    def action_view_field_jobs(self):
        self.ensure_one()
        return {"type": "ir.actions.act_window", "name": "Historia wizyt", "res_model": "instalacje24.field.job", "view_mode": "tree,form,kanban", "domain": [("partner_id", "=", self.id)]}

    def action_view_warranties(self):
        self.ensure_one()
        return {"type": "ir.actions.act_window", "name": "Gwarancje", "res_model": "instalacje24.warranty", "view_mode": "tree,form", "domain": [("partner_id", "=", self.id)]}

    def action_view_complaints(self):
        self.ensure_one()
        return {"type": "ir.actions.act_window", "name": "Reklamacje", "res_model": "instalacje24.complaint", "view_mode": "tree,form", "domain": [("partner_id", "=", self.id)]}

    @classmethod
    def _cron_seasonal_reminders(cls, env):
        month = str(fields.Date.today().month)
        partners = env["res.partner"].search([("seasonal_reminder", "=", True), ("seasonal_reminder_month", "=", month)])
        activity_type = env.ref("mail.mail_activity_data_todo")
        model_id = env["ir.model"]._get_id("res.partner")
        for partner in partners:
            env["mail.activity"].create({"res_id": partner.id, "res_model_id": model_id, "activity_type_id": activity_type.id, "summary": "Przypomnienie o serwisie kotła", "user_id": env.user.id})
