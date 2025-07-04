```markdown
# attack_exporter

`attack_exporter` downloads the current **MITRE ATT&CK Enterprise** dataset,
filters out revoked/deprecated items, and exports a small, useful CSV:

```

id,name,platforms,description,language

````

No packaging or complex setup—just one dependency (`requests`) and a few
Python files.

---

## Installation

```bash
pip install requests
git clone <repo-url>
cd attack_exporter
````

---

## Basic use

```bash
# 1. Fetch or refresh the ATT&CK bundle
python cli.py update

# 2. Export a CSV (saved as enterprise.csv)
python cli.py export csv --out enterprise
```

---

## Directory overview

| Path         | Description                                                         |
| ------------ | ------------------------------------------------------------------- |
| `cli.py`     | Command-line front-end (`update`, `export`).                        |
| `core/`      | Shared code. Contains **Fetcher**, **Parser** and **CSV exporter**. |
| `platforms/` | Light wrappers that register the generic components for each OS.    |
| `cache/`     | JSON bundle is stored here automatically.                           |

---

## Cache location

Default: `attack_exporter/cache/enterprise-attack.json`
Override with `ATTACK_EXPORTER_CACHE`:

```bash
export ATTACK_EXPORTER_CACHE="/var/tmp/attack_exporter"
python cli.py update
```

---

## Extending

* Add another export format: drop a new `core/exporter_<fmt>.py`,
  register it in `core/registry.py`, expose it in `cli.py`.
* Support a new OS: create `platforms/<os>/__init__.py` that registers the
  generic classes (or custom ones).

---

## Licence

Code: MIT
ATT\&CK content: © MITRE Corporation, CC-BY 4.0

```
```
