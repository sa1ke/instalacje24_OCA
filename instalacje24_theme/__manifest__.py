{
    "name": "Instalacje24 Theme",
    "summary": "Branding UI/PDF dla Instalacje24",
    "version": "17.0.1.0.0",
    "category": "Tools",
    "author": "Instalacje24",
    "license": "LGPL-3",
    "depends": ["web", "mail", "account", "sale_management", "instalacje24_office", "instalacje24_terrain"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/dashboard_branding_views.xml",
        "views/login_branding_templates.xml",
        "views/splash_templates.xml",
        "views/terrain_branding_views.xml",
        "report/premium_invoice_report.xml",
        "report/premium_offer_report.xml",
        "report/business_card_report.xml",
        "data/email_signature_template.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "instalacje24_theme/static/src/scss/theme_backend.scss",
        ],
        "web.assets_frontend": [
            "instalacje24_theme/static/src/scss/theme_frontend.scss",
            "instalacje24_theme/static/src/scss/splash.scss",
        ],
        "web.assets_common": [
            "instalacje24_theme/static/src/xml/splash.xml",
        ],
    },
    "application": False,
}
