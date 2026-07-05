# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-04

### Added
- Initial release: Tkinter GUI for folder backup on Windows.
- **Backup Now** — one-off copy with source and destination only.
- **Schedule backups** — interval (days) + 24-hour clock time (`HH:MM`).
- **Incremental copies** — unchanged files are skipped on repeat runs.
- **Stop** — cancel an in-progress copy or halt the scheduler.
- Live progress bar, status line, and scrollable log console.
- CSV logs under `logs/` (`copy_success.csv`, `copy_errors.csv`).
- GUI state persists between runs (`gui_state.json` next to the app).
- Standalone Windows `.exe` via PyInstaller (no Python install required).
- pytest suite for core copy/validation logic.
- GitHub Actions CI (tests + Windows build artifact).

[1.0.0]: https://github.com/stephenvowell/python-backup/releases/tag/v1.0.0
