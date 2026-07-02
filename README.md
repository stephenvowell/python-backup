# Python BackUp

Python BackUp is a small backup utility with a Tkinter GUI. You can run a **one-off backup** or **schedule** recurring copies of a folder to a destination. Results are logged to CSV files under `logs/`.

## Features

- **Browse folders**: Pick source and destination directories.
- **Backup Now**: Copy immediately using only source and destination (no schedule required).
- **Schedule backups**: Set interval (days) and **24-hour** time `HH:MM` (e.g. `09:00`, `14:30`), then **Start Backup** to run on that schedule.
- **Stop**: Cancel an in-progress copy and stop the scheduler at any time.
- **Incremental copies**: Files that already match the destination are skipped.
- **CSV logs** (appended across runs): `logs/copy_success.csv` and `logs/copy_errors.csv`. Paths are properly quoted, so commas in file paths never corrupt the columns.

## Requirements

- Python 3.x
- Tkinter (usually included with Windows/macOS Python from [python.org](https://www.python.org/))
- [`schedule`](https://pypi.org/project/schedule/)

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/stephenvowell/PythonBackUp.git
   cd PythonBackUp
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

From the project directory:

```sh
python backup_v2.py
```

### In the GUI

1. Choose **Source** and **Destination** folders (Browse or type paths).
2. Optional — **Backup Now** to copy once right away.
3. For scheduling, fill **Interval (days)** and **Time (24-hour HH:MM)**, then **Start Backup**. The scheduled job runs at that clock time; use **Backup Now** if you also need an immediate copy.
4. Press **Stop** to cancel a running copy or halt the scheduler.

On Windows PowerShell 5.x, chain commands with `;` instead of `&&`, for example:

```powershell
Set-Location C:\path\to\PythonBackUp; python backup_v2.py
```

## Project layout

- `backup_v2.py` — the Tkinter GUI application.
- `backup_core.py` — GUI-free copy/validation/logging logic (imported by the GUI and covered by tests).

## Build a standalone Windows executable

Produce a single-file `.exe` that runs without a Python install:

```powershell
pip install -r requirements-dev.txt
.\build_exe.ps1
```

The executable is written to `dist\PythonBackUp.exe`.

## Running tests

```sh
pip install -r requirements-dev.txt
pytest
```

## Contributing

Contributions are welcome. Fork the repository and open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
