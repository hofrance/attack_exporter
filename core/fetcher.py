# core/fetcher.py  (remplacer _default_cache_dir)

from pathlib import Path
import os, requests, sys
from .interfaces import Fetcher

URL = ("https://raw.githubusercontent.com/mitre/cti/master/"
       "enterprise-attack/enterprise-attack.json")

def _default_cache_dir() -> Path:
    # 1) variable d’environnement prioritaire
    if env := os.getenv("ATTACK_EXPORTER_CACHE"):
        return Path(env).expanduser()

    # 2) dossier 'cache' au niveau du dépôt
    return Path(__file__).resolve().parent.parent / "cache"

class GenericFetcher(Fetcher):
    def __init__(self):
        self.cache_path = _default_cache_dir() / "enterprise-attack.json"
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)

    def download(self, force: bool = False):
        if self.cache_path.exists() and not force:
            return self.cache_path
        print("[+] Téléchargement JSON ATT&CK…")
        r = requests.get(URL, timeout=30); r.raise_for_status()
        self.cache_path.write_bytes(r.content)
        return self.cache_path
