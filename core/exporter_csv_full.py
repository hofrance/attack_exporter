from pathlib import Path
import csv
from core.interfaces import Exporter

class GenericCSVExporterFull(Exporter):
    def export(self, rows, out_path: Path):
        # aucune troncature : rows déjà contiennent la desc complète
        out_path = out_path.with_suffix(".csv")
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)
