Voici une refonte minimaliste mais complète de `core/fetcher.py` qui :

1. **Respecte l’arborescence cache native de l’OS** (spéc XDG sous Linux, `%LOCALAPPDATA%` sous Windows, etc.).
2. **Permet de récupérer Enterprise, Mobile *et* ICS** sans dupliquer le code.
3. Garde la compatibilité avec la variable d’environnement `ATTACK_EXPORTER_CACHE`.

```python
"""
core/fetcher.py
Téléchargement et mise en cache des collections MITRE ATT&CK (STIX 2.1 JSON).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal, Final

import requests
from platformdirs import user_cache_dir    # pip install platformdirs

from .interfaces import Fetcher

# ────────────────────────────
# 1.  URLs officielles v17.1
# ────────────────────────────
MATRIX_URLS: Final[dict[Literal["enterprise", "mobile", "ics"], str]] = {
    "enterprise": "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json",  # :contentReference[oaicite:0]{index=0}
    "mobile":     "https://raw.githubusercontent.com/mitre/cti/master/mobile-attack/mobile-attack.json",          # :contentReference[oaicite:1]{index=1}
    "ics":        "https://raw.githubusercontent.com/mitre/cti/master/ics-attack/ics-attack.json",               # :contentReference[oaicite:2]{index=2}
}

# ────────────────────────────
# 2.  Répertoire de cache
# ────────────────────────────
def _default_cache_dir() -> Path:
    """
    Renvoie le dossier de cache :
    1. $ATTACK_EXPORTER_CACHE s’il existe
    2. ~/.cache/attack_exporter   (Linux/macOS)
       %LOCALAPPDATA%\\attack_exporter (Windows)
    """
    if env := os.getenv("ATTACK_EXPORTER_CACHE"):
        return Path(env).expanduser()
    return Path(user_cache_dir("attack_exporter"))

# ────────────────────────────
# 3.  Fetcher générique
# ────────────────────────────
class AttackFetcher(Fetcher):
    """Télécharge et met en cache n’importe quelle matrice ATT&CK."""

    def __init__(self, matrix: Literal["enterprise", "mobile", "ics"] = "enterprise") -> None:
        if matrix not in MATRIX_URLS:
            raise ValueError(f"Matrix « {matrix} » non supportée")
        self.matrix = matrix
        self.url = MATRIX_URLS[matrix]
        self.cache_path = _default_cache_dir() / f"{matrix}-attack.json"
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)

    # --- API publique ---------------------------------------------------------
    def download(self, force: bool = False) -> Path:
        """
        Retourne le chemin local du JSON.
        - Si le fichier existe et *force* == False ⇒ aucun appel réseau.
        - Sinon télécharge depuis GitHub (time-out 30 s).
        """
        if self.cache_path.exists() and not force:
            return self.cache_path

        print(f"[+] Téléchargement ATT&CK ({self.matrix})…")
        r = requests.get(self.url, timeout=30)
        r.raise_for_status()
        self.cache_path.write_bytes(r.content)
        return self.cache_path

# ────────────────────────────
# 4.  Utilitaires facultatifs
# ────────────────────────────
def download_all(force: bool = False) -> dict[str, Path]:
    """Télécharge Enterprise + Mobile + ICS en une seule commande."""
    return {m: AttackFetcher(m).download(force=force) for m in MATRIX_URLS}

# Exemple CLI minimal (python -m core.fetcher --matrix mobile --force)
if __name__ == "__main__":
    import argparse, sys
    p = argparse.ArgumentParser(description="Télécharge une collection ATT&CK")
    p.add_argument("--matrix", choices=MATRIX_URLS, default="enterprise",
                   help="enterprise | mobile | ics (par défaut : enterprise)")
    p.add_argument("--force", action="store_true",
                   help="forcer le re-téléchargement même si le cache existe")
    args = p.parse_args()
    try:
        path = AttackFetcher(args.matrix).download(force=args.force)
        print(f"[✓] Collection enregistrée : {path}")
    except Exception as exc:
        print(f"[✗] Erreur : {exc}", file=sys.stderr)
        sys.exit(1)
```

### Pourquoi ces choix ?

| Problème                 | Solution proposée                                                                             |
| ------------------------ | --------------------------------------------------------------------------------------------- |
| **Cache portable**       | `platformdirs.user_cache_dir()` respecte XDG /Linux, `AppData`/Windows, etc.                  |
| **Multiples matrices**   | Un dictionnaire `MATRIX_URLS` + `AttackFetcher(matrix)` évite trois classes quasi identiques. |
| **Maintenance minimale** | Mettre à jour vers v18 ? Il suffit de changer les URL dans `MATRIX_URLS`.                     |
| **Forçage / hors-ligne** | Paramètre `force` pour ignorer le cache ; sinon zéro requête HTTP.                            |
| **Extensibilité**        | Ajoutez “pre-attack” ou une URL privée en complétant simplement `MATRIX_URLS`.                |

---

#### Idées d’améliorations si besoin

* **Validation de fraîcheur** : faire un `HEAD` et comparer `ETag`/`Last-Modified` pour éviter les re-downloads inutiles mais signaler une maj.
* **`requests-cache`** : persiste les réponses HTTP et gère la validation conditionnelle (304).
* **Signatures** : vérifier le SHA-256 ou la signature PGP de la release MITRE (utile en environnements régulés).
* **Tests unitaires** : mock de `requests.get` + fichier temporaire pour valider le chemin cache.

Avec ce module, votre pipeline peut désormais exporter *toutes* les techniques et sous-techniques ATT\&CK sans changer de script — il suffit de spécifier la matrice voulue. Bonne intégration !
