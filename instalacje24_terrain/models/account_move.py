from odoo import api, fields, models


class AccountMove(models.Model):
    """Invoice QR payment placeholder for quick bank transfer mobile flows."""

    _inherit = "account.move"

    instalacje24_qr_payment_url = fields.Char(string="Link QR płatności", compute="_compute_qr_url")

    @api.depends("amount_total", "name")
    def _compute_qr_url(self):
        for rec in self:
            if rec.amount_total and rec.name:
                rec.instalacje24_qr_payment_url = f"https://example.com/qr-payment?invoice={rec.name}&amount={rec.amount_total}"
            else:
                rec.instalacje24_qr_payment_url = False
