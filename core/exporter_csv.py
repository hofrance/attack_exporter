"""Exportateur CSV minimal – commun à toutes les plateformes."""
import csv
from pathlib import Path
from .interfaces import Exporter

class GenericCSVExporter(Exporter):
    def export(self, rows, out_path: Path):
        out_path = out_path.with_suffix('.csv')
        if not rows:
            raise ValueError("rows list is empty – nothing to export")
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)
        print(f"[✓] CSV écrit : {out_path} ({len(rows)} lignes)")
