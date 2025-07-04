#!/usr/bin/env python3
import argparse, json, importlib
from pathlib import Path
from core.registry import get_provider

def _import_platforms():
    for name in ("linux", "windows"):
        try:
            importlib.import_module(f"platforms.{name}")
        except ModuleNotFoundError:
            pass

def main():
    _import_platforms()

    ap = argparse.ArgumentParser()
    ap.add_argument("--os", help="windows | linux | mac (auto if omitted)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("update")

    p_exp = sub.add_parser("export")
    p_exp.add_argument("fmt", choices=["csv"])
    p_exp.add_argument("--out", default="enterprise")

    args = ap.parse_args()
    fetcher, parser, exporter = get_provider(args.os)

    if args.cmd == "update":
        print("Downloading / refreshing ATT&CK …")
        path = fetcher.download(force=True)
        print("JSON stored at", path)
    else:
        bundle = json.load(open(fetcher.download(), encoding="utf-8"))
        rows = parser.parse(bundle)
        exporter.export(rows, Path(args.out))

if __name__ == "__main__":
    main()
