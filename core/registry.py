# core/registry.py
"""Central registry for operating-system providers and export formats."""

import sys
import importlib
from typing import Tuple

from .interfaces import Fetcher, Parser, Exporter
from .exporter_csv import GenericCSVExporter
from .exporter_csv_full import GenericCSVExporterFull

# ---------------------------------------------------------------------------
# Exporters registry
# ---------------------------------------------------------------------------

_EXPORTERS: dict[str, type[Exporter]] = {
    "csv": GenericCSVExporter,          # minimal description (truncated)
    "csv_full": GenericCSVExporterFull  # full description
}

def get_exporter(fmt: str) -> Exporter:
    """Return an *instance* of the exporter matching `fmt`."""
    try:
        return _EXPORTERS[fmt]()
    except KeyError:
        raise ValueError(f"Unsupported format '{fmt}'. "
                         f"Available: {', '.join(_EXPORTERS)}")

# ---------------------------------------------------------------------------
# Providers registry
# ---------------------------------------------------------------------------

_PROVIDERS: dict[str, Tuple[type[Fetcher], type[Parser]]] = {}

def register(os_name: str,
             fetcher: type[Fetcher],
             parser: type[Parser],
             exporter: type[Exporter] | None = None) -> None:
    """
    Register a provider for a given OS.

    - os_name  : 'windows', 'linux', 'darwin',…
    - fetcher  : class implementing Fetcher
    - parser   : class implementing Parser
    - exporter : default exporter for this OS (optional)
    """
    _PROVIDERS[os_name] = (fetcher, parser, exporter or GenericCSVExporter)

def get_provider(os_override: str | None = None
                 ) -> Tuple[Fetcher, Parser, Exporter]:
    """
    Instantiate the Fetcher, Parser and *default* Exporter for the OS.

    If you need a different export format, call `get_exporter()` separately.
    """
    target = os_override or sys.platform     # e.g. 'win32', 'linux'
    base   = "windows" if target.startswith("win") else target.split("-")[0]
    if base not in _PROVIDERS:
        raise RuntimeError(f"No provider for OS '{base}' (yet)")

    fetcher_cls, parser_cls, exporter_cls = _PROVIDERS[base]
    return fetcher_cls(), parser_cls(), exporter_cls()

# ---------------------------------------------------------------------------
# Helper: auto-import platforms so they call register() at import-time
# ---------------------------------------------------------------------------

def import_platforms() -> None:
    """Import platforms.* modules to trigger their `register()` calls."""
    for name in ("linux", "windows"):           # add 'mac', 'freebsd', …
        try:
            importlib.import_module(f"platforms.{name}")
        except ModuleNotFoundError:
            pass
