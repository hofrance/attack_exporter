import sys, importlib
from .interfaces import Fetcher, Parser, Exporter

_PROVIDERS = {}

def register(os_name: str, fetcher, parser, exporter):
    _PROVIDERS[os_name] = (fetcher, parser, exporter)

def get_provider(target_os: str | None = None):
    target = target_os or sys.platform      # ex. 'win32', 'linux'
    base = 'windows' if target.startswith('win') else target.split('-')[0]
    if base not in _PROVIDERS:
        raise RuntimeError(f"No provider for OS '{base}' (yet)")
    f, p, e = _PROVIDERS[base]
    return f(), p(), e()                    # instances
