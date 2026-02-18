from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    instalacje24_brand_logo = fields.Image(
        string="Logo Instalacje24",
        related="company_id.logo",
        readonly=False,
    )
    instalacje24_brand_primary = fields.Char(
        string="Kolor główny",
        config_parameter="instalacje24_theme.brand_primary",
        default="#0E3A53",
    )
    instalacje24_brand_secondary = fields.Char(
        string="Kolor dodatkowy",
        config_parameter="instalacje24_theme.brand_secondary",
        default="#2DB3E8",
    )
    instalacje24_brand_accent = fields.Char(
        string="Kolor akcentu",
        config_parameter="instalacje24_theme.brand_accent",
        default="#F59C2D",
    )
    instalacje24_brand_background = fields.Char(
        string="Kolor tła",
        config_parameter="instalacje24_theme.brand_background",
        default="#E6ECEF",
    )
    instalacje24_services_line = fields.Char(
        string="Linia usług (wizytówka/email)",
        config_parameter="instalacje24_theme.services_line",
        default="Instalacje wod-kan • Ogrzewanie • Serwis kotłów",
    )
    instalacje24_business_phone = fields.Char(
        string="Telefon na wizytówce/email",
        config_parameter="instalacje24_theme.business_phone",
        default="+48 600 000 000",
    )
    instalacje24_business_website = fields.Char(
        string="WWW na wizytówce/email",
        config_parameter="instalacje24_theme.business_website",
        default="https://instalacje24.example.com",
    )
    instalacje24_whatsapp = fields.Char(
        string="WhatsApp (wa.me)",
        config_parameter="instalacje24_theme.business_whatsapp",
        default="https://wa.me/48600000000",
    )
    instalacje24_maps = fields.Char(
        string="Google Maps URL",
        config_parameter="instalacje24_theme.business_maps",
        default="https://maps.google.com",
    )
