#!/usr/bin/env python3
"""
core/exporter_csv.py
--------------------

Two CSV exporters that implement the « Exporter » interface:

* GenericCSVExporter       – truncated *description* field (180 chars)
* GenericCSVExporterFull   – full *description* field

Both work on any operating system; the path is resolved by the caller.
"""

from __future__ import annotations

import csv
import textwrap
from pathlib import Path
from typing import List, Dict

from .interfaces import Exporter


class _BaseCSVExporter(Exporter):
    """Common helper code for all CSV exporters."""

    #: number of characters kept in the description for the *minimal* variant
    _DESC_WIDTH: int | None = None  # None ⇒ no truncation

    # ------------------------------------------------------------------ #
    # public API                                                         #
    # ------------------------------------------------------------------ #
    def export(self, rows: List[Dict[str, str]], out_path: Path) -> None:
        """Write *rows* to « *out_path*.csv » (UTF-8, RFC 4180)."""
        if not rows:
            raise ValueError("rows list is empty – nothing to export")

        out_path = out_path.with_suffix(".csv")
        processed = self._rows_for_csv(rows)

        with open(out_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=processed[0].keys())
            writer.writeheader()
            writer.writerows(processed)

        print(f"[✓] CSV written : {out_path} ({len(processed)} rows)")

    # ------------------------------------------------------------------ #
    # internal helpers                                                   #
    # ------------------------------------------------------------------ #
    def _rows_for_csv(
        self, rows: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """Return a copy of *rows* with description possibly shortened."""
        if self._DESC_WIDTH is None:
            return rows  # full description variant

        out: List[Dict[str, str]] = []
        for row in rows:
            new_row = row.copy()
            new_row["desc"] = textwrap.shorten(
                row["desc"], width=self._DESC_WIDTH, placeholder="…"
            )
            out.append(new_row)
        return out


class GenericCSVExporter(_BaseCSVExporter):
    """Keeps the description short (180 characters)."""

    _DESC_WIDTH = 180


class GenericCSVExporterFull(_BaseCSVExporter):
    """Keeps the complete description (no truncation)."""

    _DESC_WIDTH = None
