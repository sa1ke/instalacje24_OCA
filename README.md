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


## Installation fix (Odoo 17)
Resolved startup error:
`External ID not found in the system: instalacje24_terrain.action_instalacje24_service_template`.

### Root cause
`instalacje24_terrain/views/menu_views.xml` was loaded before views that define action IDs.
On clean databases, menu XML referenced actions that were not loaded yet.

### Fix
- Kept XML IDs unchanged (data compatibility).
- Reordered `instalacje24_terrain` manifest data load so action/view files load before `menu_views.xml`.
- Bumped module version to `17.0.2.1.0`.

### Safe upgrade steps
1. Update module code in your addons path.
2. Restart Odoo service.
3. Upgrade modules in order:
   - `instalacje24_terrain`
   - `instalacje24_office`
   - `instalacje24_ai_quote` (if installed)
   - `instalacje24_theme` (if installed)
4. If Apps list is stale, run **Update Apps List** first.
