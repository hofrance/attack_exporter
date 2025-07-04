#!/usr/bin/env python3
"""
cli.py – single entry-point for attack_exporter

Commands
--------
update                Download / refresh the ATT&CK Enterprise bundle.
export <fmt>          Export the parsed data in the chosen format.

Options
-------
--os <windows|linux|mac>   Force a provider (auto-detected if omitted).
--out <path>               Output file stem (extension is added automatically).
"""

import argparse
import importlib
import json
from pathlib import Path

from core.registry import get_provider


def _import_platforms() -> None:
    """Import platform packages so their `register()` calls run."""
    for name in ("linux", "windows"):      # Add 'mac', 'freebsd', … when ready
        try:
            importlib.import_module(f"platforms.{name}")
        except ModuleNotFoundError:
            # Platform not implemented yet – ignore silently
            pass


def build_parser() -> argparse.ArgumentParser:
    """Return a fully configured ArgumentParser."""
    ap = argparse.ArgumentParser(prog="attack-export")
    ap.add_argument(
        "--os",
        metavar="OS",
        help="windows | linux | mac (auto-detected if omitted)",
    )

    sub = ap.add_subparsers(dest="cmd", required=True)

    # update
    sub.add_parser("update", help="Download / refresh ATT&CK JSON cache")

    # export
    p_exp = sub.add_parser("export", help="Export data")
    p_exp.add_argument(
        "fmt",
        choices=["csv", "csv_full"],
        help="csv = truncated description, csv_full = full description",
    )
    p_exp.add_argument(
        "--out",
        default="enterprise",
        help='Output file stem (e.g. "report" -> report.csv)',
    )

    return ap


def main() -> None:
    _import_platforms()

    parser = build_parser()
    args = parser.parse_args()

    fetcher, parser_, exporter_default = get_provider(args.os)

    if args.cmd == "update":
        print("Downloading / refreshing ATT&CK JSON …")
        path = fetcher.download(force=True)
        print("JSON stored at", path)
        return

    # --- export ---
    bundle = json.load(open(fetcher.download(), encoding="utf-8"))
    rows = parser_.parse(bundle)

    # Let the registry give us the correct exporter class for fmt
    from core.registry import get_exporter   # local import to avoid cycle
    exporter = get_exporter(args.fmt)

    exporter.export(rows, Path(args.out))


if __name__ == "__main__":
    main()
