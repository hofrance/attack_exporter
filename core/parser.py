"""Parseur générique ATT&CK Enterprise – OS-agnostique."""
import textwrap
from typing import List, Dict, Any
from .interfaces import Parser

class GenericParser(Parser):
    """Renvoie une liste de dict minimalistes (id, name, platforms, desc)."""
    def parse(self, bundle_json: Dict[str, Any]) -> List[Dict[str, Any]]:
        rows = []
        for obj in bundle_json.get("objects", []):
            if obj.get("type") != "attack-pattern":
                continue
            if obj.get("revoked") or obj.get("x_mitre_deprecated"):
                continue

            mitre_id = next(
                (ref["external_id"] for ref in obj.get("external_references", [])
                 if ref.get("source_name") == "mitre-attack"),
                obj.get("id")
            )
            # core/parser.py  – ne garder que la partie modifiée
            rows.append({
                "id": mitre_id,
                "name": obj.get("name", ""),
                "platforms": ", ".join(obj.get("x_mitre_platforms", [])),
                "desc": textwrap.shorten(
                    obj.get("description", "").replace("\n", " "), 180, placeholder="…"
                )
            })

        return rows
