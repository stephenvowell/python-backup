"""Core, GUI-free backup logic for Python BackUp.

Kept separate from ``backup_v2.py`` so it can be imported and unit-tested
without launching Tkinter. Handles the file copy, time validation, and
CSV logging (append mode with proper quoting so paths containing commas
never corrupt the log).
"""

import csv
import datetime
import filecmp
import os
import re
import shutil

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
SUCCESS_LOG = os.path.join(LOG_DIR, "copy_success.csv")
ERROR_LOG = os.path.join(LOG_DIR, "copy_errors.csv")

SUCCESS_HEADER = ["Timestamp", "Message"]
ERROR_HEADER = ["Timestamp", "Level", "Message"]

_TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


def ensure_log_dir():
    os.makedirs(LOG_DIR, exist_ok=True)


def _now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _append_csv(path, header, row):
    """Append a row, writing the header first only when the file is new/empty."""
    ensure_log_dir()
    is_new = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(header)
        writer.writerow(row)


def log_success(message):
    _append_csv(SUCCESS_LOG, SUCCESS_HEADER, [_now(), message])


def log_error(message):
    _append_csv(ERROR_LOG, ERROR_HEADER, [_now(), "ERROR", message])


def validate_time_format(time_str):
    """True only for a valid 24-hour ``HH:MM`` string (00:00–23:59)."""
    return _TIME_RE.match(time_str or "") is not None


def copy_folder(src, dst, progress_cb=None, cancel_event=None):
    """Copy the tree at ``src`` into ``dst``, skipping files already identical.

    ``progress_cb(done, total)`` is called after each file. If ``cancel_event``
    is provided and set, the copy stops early and ``cancelled`` is returned True.
    """
    if not os.path.exists(dst):
        os.makedirs(dst)

    total = sum(len(files) for _, _, files in os.walk(src))
    done = copied = unchanged = errors = 0
    cancelled = False

    def report():
        if progress_cb:
            progress_cb(done, total)

    for dirpath, _dirs, files in os.walk(src):
        if cancel_event is not None and cancel_event.is_set():
            cancelled = True
            break
        for file in files:
            if cancel_event is not None and cancel_event.is_set():
                cancelled = True
                break
            src_file = os.path.join(dirpath, file)
            dst_file = os.path.join(dst, os.path.relpath(src_file, src))
            try:
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                if not os.path.exists(dst_file) or not filecmp.cmp(src_file, dst_file, shallow=False):
                    shutil.copy2(src_file, dst_file)
                    log_success(f"Copied {src_file} to {dst_file}")
                    copied += 1
                else:
                    unchanged += 1
            except Exception as e:  # noqa: BLE001 - log and continue on any file error
                errors += 1
                log_error(f"Failed to copy {src_file} to {dst_file}: {e}")
            done += 1
            report()
        if cancelled:
            break

    if total == 0 and progress_cb:
        progress_cb(0, 0)

    return {
        "errors": errors,
        "copied": copied,
        "unchanged": unchanged,
        "total": total,
        "cancelled": cancelled,
    }
