# Instalacje24 Odoo 17 Community Suite

Production-ready repository for a one-person plumbing business on Odoo 17 Community.

## Modules

- `instalacje24_office` – CRM, wyceny, szybkie zlecenia, estimator, dashboard biurowy.
- `instalacje24_terrain` – teren/tablet, czas pracy, materiały, gwarancje, reklamacje, projekty.
- `instalacje24_ai_quote` – asystent rule-based + opcjonalny OpenAI (gdy API key istnieje).

## Quick install

1. Copy module folders to `/custom-addons`:
   - `instalacje24_terrain`
   - `instalacje24_office`
   - `instalacje24_ai_quote` (opcjonalnie)
2. Update Apps List.
3. Install order:
   1. `Instalacje24 Terrain`
   2. `Instalacje24 Office`
   3. `Instalacje24 AI Quote` (optional)
4. Assign user to **Instalacje24 User** group.

## Core workflow (daily)

1. CRM lead / szybkie nowe zlecenie.
2. Kalkulator + quick pricing / AI suggest.
3. Utworzenie zlecenia terenowego.
4. START/STOP, materiały, zdjęcia, podpis na tablecie.
5. Zakończ + faktura draft 1 klik.

## Included business features

- Android tablet UX (duże przyciski, sticky header, dark mode, szybkie akcje).
- JDG automations (24h reminder, unpaid 7d, recurring jobs, seasonal reminders).
- Warranty + complaint system.
- Installation project mode with checklist and Gantt.
- Material profitability analysis and margin alerts.
- House-size installation estimator with configurable formulas.
- WhatsApp quick links and route links.
- Offline draft/retry placeholders + backup ZIP/CSV export.
- Reports: revenue/profit/time/complaints/material usage/km.

## Pricing and services

- Global pricing and estimator formulas in Settings → Sales → Instalacje24.
- Service templates define fixed prices and default materials.
- Quick buttons in quote form for common plumbing services.

## Additional docs

- `HOW_TO_INSTALL.md`
- `HOW_TO_CUSTOMIZE_PRICING.md`
- `UX_IMPROVEMENTS.md`
- `AUTOMATION_RULES.md`
- `HOW_TO_USE_TABLET.md`
- `HOW_TO_ADJUST_ESTIMATOR.md`


## Branding & UI (instalacje24_theme)
- Zainstaluj moduł `instalacje24_theme`, aby aktywować branding (navbar, dashboard cards, tablet header, dark mode, premium PDF, splash).
- Umieść logo firmy w `branding/logo.png` (repo root). Jeśli brak logo, moduł użyje neutralnego fallbacku kolorów.
- Kolory marki i zasady znajdziesz w `BRAND_COLORS.md` i `BRAND_GUIDE.md`.
- Konfiguracja podpisu email/wizytówki/kolorów: **Ustawienia > Instalacje24 Branding**.
