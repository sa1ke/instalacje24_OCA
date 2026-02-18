import base64
import csv
import io
import zipfile
from odoo import fields, models


class Instalacje24BackupService(models.Model):
    """Technical helper model to build weekly backup attachments by cron."""

    _name = "instalacje24.backup.service"
    _description = "Serwis backupu"

    name = fields.Char(default="Backup Service")

    def _build_zip(self):
        jobs = self.env["instalacje24.field.job"].search([])
        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(["id", "name", "partner", "state", "profit"])
        for j in jobs:
            writer.writerow([j.id, j.name, j.partner_id.display_name, j.state, j.profit_amount])

        mem = io.BytesIO()
        with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("jobs.csv", out.getvalue().encode())
        return mem.getvalue()

    @classmethod
    def _cron_weekly_backup(cls, env):
        payload = env["instalacje24.backup.service"]._build_zip()
        env["ir.attachment"].create({
            "name": f"instalacje24_weekly_{fields.Date.today()}.zip",
            "datas": base64.b64encode(payload),
            "mimetype": "application/zip",
            "type": "binary",
        })
