import base64
import csv
import io
import zipfile
from odoo import fields, models


class Instalacje24BackupExport(models.TransientModel):
    """Generate simple ZIP backup with CSV exports for jobs and materials."""

    _name = "instalacje24.backup.export"
    _description = "Eksport backupu"

    name = fields.Char(default="instalacje24_backup.zip")
    file_data = fields.Binary(string="Plik", readonly=True)

    def action_generate(self):
        self.ensure_one()
        jobs = self.env["instalacje24.field.job"].search([])
        materials = self.env["instalacje24.field.material"].search([])

        def _csv(rows, headers):
            out = io.StringIO()
            writer = csv.writer(out)
            writer.writerow(headers)
            writer.writerows(rows)
            return out.getvalue().encode()

        job_rows = [[j.id, j.name, j.partner_id.display_name, j.state, j.duration, j.profit_amount] for j in jobs]
        material_rows = [[m.id, m.job_id.display_name, m.product_id.display_name, m.quantity] for m in materials]

        mem = io.BytesIO()
        with zipfile.ZipFile(mem, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("jobs.csv", _csv(job_rows, ["id", "name", "partner", "state", "duration", "profit"]))
            zf.writestr("materials.csv", _csv(material_rows, ["id", "job", "product", "qty"]))

        self.file_data = base64.b64encode(mem.getvalue())
        return {
            "type": "ir.actions.act_window",
            "res_model": "instalacje24.backup.export",
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }
