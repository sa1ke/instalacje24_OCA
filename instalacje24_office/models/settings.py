from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Global pricing and estimator settings for fast daily operations."""

    _inherit = "res.config.settings"

    instalacje24_hourly_rate = fields.Float(string="Domyślna stawka/h", config_parameter="instalacje24_office.hourly_rate")
    instalacje24_travel_rate = fields.Float(string="Domyślna stawka/km", config_parameter="instalacje24_office.travel_rate")
    instalacje24_margin_percent = fields.Float(string="Domyślna marża %", config_parameter="instalacje24_office.margin_percent")
    instalacje24_vat_percent = fields.Float(string="Domyślny VAT %", config_parameter="instalacje24_office.vat_percent")
    instalacje24_quick_price_repair = fields.Float(string="Szybka naprawa", config_parameter="instalacje24_office.quick_price_repair")
    instalacje24_quick_price_boiler = fields.Float(string="Serwis kotła", config_parameter="instalacje24_office.quick_price_boiler")
    instalacje24_quick_price_installation = fields.Float(string="Montaż instalacji", config_parameter="instalacje24_office.quick_price_installation")

    instalacje24_estimator_base_m2 = fields.Float(string="Estimator: koszt materiału/m2", config_parameter="instalacje24_office.estimator_base_m2")
    instalacje24_estimator_bathroom_factor = fields.Float(string="Estimator: łazienka", config_parameter="instalacje24_office.estimator_bathroom_factor")
    instalacje24_estimator_floor_factor = fields.Float(string="Estimator: kondygnacja", config_parameter="instalacje24_office.estimator_floor_factor")
    instalacje24_estimator_labor_per_m2 = fields.Float(string="Estimator: roboczogodziny/m2", config_parameter="instalacje24_office.estimator_labor_per_m2")

    instalacje24_min_margin_percent = fields.Float(string="Min. marża alert %", config_parameter="instalacje24_terrain.min_margin_percent")
