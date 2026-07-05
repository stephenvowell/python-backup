# Python BackUp

[![CI](https://github.com/stephenvowell/python-backup/actions/workflows/ci.yml/badge.svg)](https://github.com/stephenvowell/python-backup/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

Python BackUp is a small backup utility with a Tkinter GUI. Run a **one-off backup**
or **schedule** recurring copies of a folder to a destination. Results are logged to
CSV files under `logs/`.

## Download (Windows)

No Python required — grab the latest standalone build:

**[Download PythonBackUp-windows.zip](https://github.com/stephenvowell/python-backup/releases/latest)**

Unzip and follow `SETUP.txt`. Licensed builds also available on
[Gumroad](https://vowellstephen.gumroad.com/l/tbmyl) · [stephenv.net](https://stephenv.net/#apps).

## Features

- **Browse folders**: Pick source and destination directories.
- **Backup Now**: Copy immediately using only source and destination (no schedule required).
- **Schedule backups**: Set interval (days) and **24-hour** time `HH:MM` (e.g. `09:00`, `14:30`), then **Start Backup** to run on that schedule.
- **Stop**: Cancel an in-progress copy and stop the scheduler at any time.
- **Incremental copies**: Files that already match the destination are skipped.
- **CSV logs** (appended across runs): `logs/copy_success.csv` and `logs/copy_errors.csv`. Paths are properly quoted, so commas in file paths never corrupt the columns.

## Requirements (from source)

- Python 3.9+
- Tkinter (usually included with Windows/macOS Python from [python.org](https://www.python.org/))
- [`schedule`](https://pypi.org/project/schedule/)

## Installation (from source)

```sh
git clone https://github.com/stephenvowell/python-backup.git
cd python-backup
pip install -r requirements.txt
python backup_v2.py
```

### In the GUI

1. Choose **Source** and **Destination** folders (Browse or type paths).
2. Optional — **Backup Now** to copy once right away.
3. For scheduling, fill **Interval (days)** and **Time (24-hour HH:MM)**, then **Start Backup**. The scheduled job runs at that clock time; use **Backup Now** if you also need an immediate copy.
4. Press **Stop** to cancel a running copy or halt the scheduler.

## Project layout

- `backup_v2.py` — the Tkinter GUI application.
- `backup_core.py` — GUI-free copy/validation/logging logic (imported by the GUI and covered by tests).
- `version.py` — release version string.
- `release/` — customer-facing `SETUP.txt` and `README.txt` bundled into the Windows zip.

## Build a standalone Windows executable

```powershell
pip install -r requirements-dev.txt
.\build_exe.ps1
```

The executable is written to `dist\PythonBackUp.exe`.

### Release zip (exe + SETUP.txt + README.txt)

```powershell
.\scripts\build-release.ps1
```

Produces `dist\PythonBackUp-windows.zip` ready for GitHub Releases or Gumroad.

## Running tests

```sh
pip install -r requirements-dev.txt
pytest
```

## Contributing

Contributions are welcome. Fork the repository and open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

© Stephen Vowell · [stephenv.net](https://stephenv.net)
