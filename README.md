# attack_exporter

**attack_exporter** is a lightweight utility that downloads the latest [MITRE ATT&CK® Enterprise](https://attack.mitre.org/) dataset, removes any revoked or deprecated items, and exports a concise CSV:

```csv
id,name,platforms,description,language
````

There’s no heavy packaging or complex setup—just one dependency (`requests`) and a few Python files.



## Installation

```bash
pip install requests
git clone https://github.com/hofrance/attack_exporter.git
cd attack_exporter
```



## Basic usage

1. **Fetch or refresh** the ATT\&CK bundle:

   ```bash
   python<your python version> cli.py update
   ```

2. **Export** the CSV (default file name: `enterprise.csv`):

   ```bash
   python cli.py export csv --out enterprise
   ```
   ``bash
     python3 cli.py export csv_full  --out enterprise-full
   ```



## Project layout

| Path/Dir     | Purpose                                                                     |
| ------------ | --------------------------------------------------------------------------- |
| `cli.py`     | Command-line entry point (`update`, `export`).                              |
| `core/`      | Shared code: contains **Fetcher**, **Parser**, and **CSVExporter** classes. |
| `platforms/` | Thin wrappers that register the generic components for each supported OS.   |
| `cache/`     | Automatically created directory where the JSON bundle is stored.            |

---

## Cache location

Default path:

```
attack_exporter/cache/enterprise-attack.json
```

Override via the `ATTACK_EXPORTER_CACHE` environment variable:

```bash
export ATTACK_EXPORTER_CACHE="/var/tmp/attack_exporter"
python cli.py update
```



## Extending

* **Add another export format:**
  Create `core/exporter_<fmt>.py`, register it in `core/registry.py`, and expose it in `cli.py`.
* **Support a new OS:**
  Add `platforms/<os>/__init__.py` that registers the generic classes (or custom ones).



## License

* **Code:** MIT
* **ATT\&CK content:** © MITRE Corporation, CC BY 4.0

