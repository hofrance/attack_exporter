# Provider Windows

Implémentations :

| Fichier | Rôle |
|---------|------|
| **fetcher.py** | Télécharge *enterprise-attack.json* dans `%LOCALAPPDATA%\attack_exporter\`. |
| **parser.py** | Filtre *revoked/deprecated*, extrait `id`, `name`, `platforms`, `description`. |
| **exporter_csv.py** | Écrit un CSV minimal (`.csv`) encodé UTF-8. |
| **\_\_init\_\_.py** | Registre le triplet (Fetcher, Parser, Exporter) via `core.registry.register("windows", …)` |

## Utilisation locale rapide

```powershell
# Dépendance
pip install requests

# Récupération + export
python ..\..\cli.py update   --os windows
python ..\..\cli.py export csv --out enterprise_win.csv --os windows
````

> Le cache se trouve dans `%LOCALAPPDATA%\attack_exporter\enterprise-attack.json`.

````