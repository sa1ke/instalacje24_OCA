import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class Instalacje24QuoteAiLog(models.Model):
    """Store AI/rule suggestions to keep transparent audit trail."""

    _name = "instalacje24.quote.ai.log"
    _description = "Log sugestii AI wyceny"

    quote_id = fields.Many2one("instalacje24.quote", string="Wycena", required=True)
    source = fields.Selection([("rule", "Rule"), ("openai", "OpenAI")], default="rule")
    suggestion = fields.Text(string="Sugestia")


class Instalacje24Quote(models.Model):
    _inherit = "instalacje24.quote"

    ai_suggestion = fields.Text(string="Sugestia AI")

    def action_ai_suggest_quote(self):
        for rec in self:
            text = (rec.lead_id.description or "").lower()
            suggestion, service = self._rule_suggest(text)
            source = "rule"
            api_key = self.env["ir.config_parameter"].sudo().get_param("instalacje24_ai_quote.openai_api_key")
            if api_key:
                # Optional integration placeholder - no hard dependency.
                source = "openai"
                suggestion = f"[OpenAI optional] {suggestion}"
            rec.ai_suggestion = suggestion
            rec.service_type = service
            self.env["instalacje24.quote.ai.log"].create({"quote_id": rec.id, "source": source, "suggestion": suggestion})

    @api.model
    def _rule_suggest(self, text):
        rules = [
            (("wyciek", "cieknie", "kapie"), "quick", "Sugerowana szybka naprawa: 1-2h + uszczelnienie/syfon."),
            (("kocioł", "piec", "serwis"), "boiler", "Sugerowany serwis kotła: czyszczenie + test szczelności."),
            (("instalacja", "dom", "podłogówka"), "installation", "Sugerowany montaż instalacji: najpierw wizja lokalna."),
        ]
        for keywords, service, message in rules:
            if any(word in text for word in keywords):
                return message, service
        return "Brak pewności – zalecana wizja lokalna i szybka wycena standard.", "quick"
