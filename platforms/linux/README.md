# Provider Linux

Implémentations :

| Fichier | Rôle |
|---------|------|
| **fetcher.py** | Télécharge le JSON ATT&CK dans `~/.cache/attack_exporter/`. |
| **parser.py**  | Nettoie et normalise les objets *attack-pattern*. |
| **exporter_csv.py** | Génère un CSV minimal encodé UTF-8. |
| **\_\_init\_\_.py** | Enregistre le provider Linux dans `core.registry`. |

## Exemple

```bash
pip install --user requests

python ../../cli.py update            # auto-détection linux
python ../../cli.py export csv --out enterprise_linux.csv
````

> Cache : `~/.cache/attack_exporter/enterprise-attack.json`