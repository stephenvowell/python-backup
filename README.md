# Python BackUp

Python BackUp is a small backup utility with a Tkinter GUI. You can run a **one-off backup** or **schedule** recurring copies of a folder to a destination. **`backup_v2.py`** is the recommended version: it logs copy results to CSV files under `logs/`. **`backupv1.py`** is an older variant without those CSV logs.

## Features

- **Browse folders**: Pick source and destination directories.
- **Backup Now**: Copy immediately using only source and destination (no schedule required).
- **Schedule backups**: Set interval (days) and **24-hour** time `HH:MM` (e.g. `09:00`, `14:30`), then **Start Backup** to run on that schedule.
- **CSV logs** (`backup_v2.py`): `logs/copy_success.csv` and `logs/copy_errors.csv`.

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

From the project directory, run the version you want:

**Recommended (CSV logs, Backup Now):**

```sh
python backup_v2.py
```

**Older GUI (no CSV logs):**

```sh
python backupv1.py
```

### In the GUI

1. Choose **Source** and **Destination** folders (Browse or type paths).
2. Optional — **Backup Now** to copy once right away.
3. For scheduling, fill **Interval (days)** and **Time (24-hour HH:MM)**, then **Start Backup**. The scheduled job runs at that clock time; use **Backup Now** if you also need an immediate copy.

On Windows PowerShell 5.x, chain commands with `;` instead of `&&`, for example:

```powershell
Set-Location C:\path\to\PythonBackUp; python backup_v2.py
```

## Contributing

Contributions are welcome. Fork the repository and open a pull request.

## License

This project is licensed under the MIT License.
