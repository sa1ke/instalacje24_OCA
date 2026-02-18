from odoo import fields, models


class Instalacje24OfflineDraft(models.Model):
    """Offline payload cache to store unsynced job edits from tablet sessions."""

    _name = "instalacje24.offline.draft"
    _description = "Szkic offline"

    name = fields.Char(string="Nazwa", required=True)
    user_id = fields.Many2one("res.users", string="Użytkownik", default=lambda self: self.env.user, required=True)
    payload_json = fields.Text(string="Dane JSON")
    state = fields.Selection([("draft", "Szkic"), ("retry", "Ponów"), ("synced", "Zsynchronizowano")], default="draft")
