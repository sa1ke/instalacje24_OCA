# AUTOMATION_RULES

## Zaimplementowane reguły

1. **Po zakończeniu zlecenia** (`action_mark_done`):
   - oznaczenie jako done,
   - automatyczne tworzenie faktury roboczej,
   - automatyczne utworzenie gwarancji.

2. **Przypomnienie 24h przed wizytą**
   - cron: `cron_visit_reminder_24h`
   - tworzy aktywność TODO dla użytkownika.

3. **Przypomnienie po 7 dniach bez płatności**
   - cron: `cron_unpaid_7d`
   - tworzy aktywność TODO dla użytkownika.

4. **Przypomnienia sezonowe**
   - cron partnerów: `cron_seasonal_reminders`.

5. **Gwarancje kończące się**
   - cron: `cron_warranty_expiring`
   - statusy active/expiring/expired.

6. **Duplikowanie poprzedniego zlecenia klienta**
   - akcja: `action_duplicate_previous_for_partner`.

7. **Quick service buttons + fixed prices**
   - szybkie ceny w wycenie + szablony usług terenowych.

8. **Auto materiały wg szablonu usługi**
   - onchange `service_template_id` dodaje pozycje materiałowe.
