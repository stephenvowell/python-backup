import os
import time
import json
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import schedule

from backup_core import copy_folder, validate_time_format, log_error, LOG_DIR, app_dir

os.makedirs(LOG_DIR, exist_ok=True)

copy_lock = threading.Lock()
# Signals the running manual/scheduled copy to stop early.
cancel_event = threading.Event()
# Signals the scheduler loop to exit.
stop_event = threading.Event()

_STATE_FILE = os.path.join(app_dir(), "gui_state.json")


def start_backup(src, dst, interval, time_str):
    def job():
        print("Job started")
        cancel_event.clear()
        ready = threading.Event()

        def ping_ui():
            set_status("Running scheduled backup…", "blue")
            progress_bar.configure(maximum=100)
            progress_var.set(0)
            ready.set()

        root.after(0, ping_ui)
        if not ready.wait(timeout=30):
            log_error("Scheduled backup: UI did not respond in time")
            print("Scheduled backup: UI ping timed out")
            return

        def progress_cb(done, total):
            root.after(0, lambda d=done, t=total: apply_progress(d, t))

        try:
            with copy_lock:
                stats = copy_folder(src, dst, progress_cb=progress_cb, cancel_event=cancel_event)
            root.after(0, lambda s=stats: finish_backup_ui(s, None, scheduled=True))
        except Exception as e:
            root.after(0, lambda err=str(e): finish_backup_ui(None, err, scheduled=True))
        print("Job completed")

    print(f"Scheduling job at {time_str}")
    if not validate_time_format(time_str):
        log_error(f"Invalid time format: {time_str}")
        print(f"Invalid time format: {time_str}")
        return
    schedule.every(interval).days.at(time_str).do(job)
    while not stop_event.is_set():
        schedule.run_pending()
        time.sleep(1)
    schedule.clear()
    print("Scheduler stopped")


root = tk.Tk()
root.title("Backup Scheduler for Python V2")
# Source folder
tk.Label(root, text="Source Folder:").grid(row=0, column=0, padx=10, pady=5)
src_entry = tk.Entry(root, width=50)
src_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: browse_folder(src_entry)).grid(row=0, column=2, padx=10, pady=5)
# Destination folder
tk.Label(root, text="Destination Folder:").grid(row=1, column=0, padx=10, pady=5)
dst_entry = tk.Entry(root, width=50)
dst_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: browse_folder(dst_entry)).grid(row=1, column=2, padx=10, pady=5)
# Interval (days)
tk.Label(root, text="Interval (days):").grid(row=2, column=0, padx=10, pady=5)
interval_entry = tk.Entry(root, width=50)
interval_entry.grid(row=2, column=1, padx=10, pady=5)
# Time — 24-hour clock
tk.Label(root, text="Time (24-hour HH:MM):").grid(row=3, column=0, padx=10, pady=5)
time_entry = tk.Entry(root, width=50)
time_entry.grid(row=3, column=1, padx=10, pady=5)
# Progress
progress_var = tk.DoubleVar(value=0)
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, mode="determinate", length=400)
progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=(10, 4), sticky="ew")
status_var = tk.StringVar(value="Ready")
status_label = tk.Label(root, textvariable=status_var, anchor="w", fg="gray")
status_label.grid(row=5, column=0, columnspan=3, padx=10, pady=(0, 8), sticky="ew")
btn_row = tk.Frame(root)
btn_row.grid(row=6, column=1, pady=12)
backup_now_btn = tk.Button(btn_row, text="Backup Now")
start_backup_btn = tk.Button(btn_row, text="Start Backup")
stop_btn = tk.Button(btn_row, text="Stop")
backup_now_btn.pack(side=tk.LEFT, padx=5)
start_backup_btn.pack(side=tk.LEFT, padx=5)
stop_btn.pack(side=tk.LEFT, padx=5)
root.columnconfigure(1, weight=1)


def load_gui_state():
    try:
        with open(_STATE_FILE, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError, TypeError):
        return
    for key, entry in (
        ("src", src_entry),
        ("dst", dst_entry),
        ("interval", interval_entry),
        ("time", time_entry),
    ):
        val = data.get(key)
        if val and isinstance(val, str):
            entry.insert(0, val)


def save_gui_state():
    data = {
        "src": src_entry.get(),
        "dst": dst_entry.get(),
        "interval": interval_entry.get(),
        "time": time_entry.get(),
    }
    try:
        with open(_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError:
        pass


def browse_folder(entry):
    initial = entry.get().strip()
    initialdir = initial if initial and os.path.isdir(initial) else None
    folder_selected = filedialog.askdirectory(initialdir=initialdir)
    if not folder_selected:
        return
    entry.delete(0, tk.END)
    entry.insert(0, folder_selected)
    print(f"Selected folder: {folder_selected}")
    save_gui_state()


load_gui_state()


def apply_progress(done, total):
    if total <= 0:
        progress_bar.configure(maximum=1)
        progress_var.set(1)
    else:
        progress_bar.configure(maximum=total)
        progress_var.set(done)


def set_status(text, color="gray"):
    status_var.set(text)
    status_label.configure(fg=color)


def begin_manual_backup_ui():
    set_status("Copying…", "blue")
    progress_bar.configure(maximum=100)
    progress_var.set(0)
    backup_now_btn.configure(state=tk.DISABLED)


def finish_backup_ui(stats, err, scheduled=False):
    backup_now_btn.configure(state=tk.NORMAL)
    if err:
        apply_progress(0, 1)
        progress_var.set(0)
        set_status(f"Failed: {err}", "red")
        messagebox.showerror("Backup", f"Backup failed:\n{err}")
        return
    if stats.get("cancelled"):
        set_status(
            f"Stopped — {stats['copied']} copied, {stats['unchanged']} unchanged before cancel.",
            "darkorange",
        )
        return
    if stats["total"] <= 0:
        apply_progress(1, 1)
        progress_var.set(1)
    if stats["errors"] == 0:
        msg = (
            f"Success — {stats['copied']} copied, {stats['unchanged']} already up to date"
            f" ({stats['total']} files)."
        )
        set_status(msg, "green")
    else:
        msg = (
            f"Finished with {stats['errors']} error(s). "
            f"{stats['copied']} copied, {stats['unchanged']} unchanged. See logs."
        )
        set_status(msg, "darkred")
        title = "Scheduled backup" if scheduled else "Backup"
        messagebox.showwarning(title, msg)


def on_start():
    src = src_entry.get()
    dst = dst_entry.get()
    interval_raw = interval_entry.get()
    time_str = time_entry.get()
    if not src or not dst or not interval_raw or not time_str:
        messagebox.showerror("Error", "All fields are required")
        print("Error: All fields are required")
        return
    try:
        interval = int(interval_raw)
        if interval <= 0:
            raise ValueError("interval must be positive")
    except ValueError:
        messagebox.showerror("Error", "Interval must be a positive whole number of days.")
        return
    if not validate_time_format(time_str):
        messagebox.showerror("Error", "Invalid time format. Use 24-hour HH:MM (e.g. 14:30).")
        print(f"Error: Invalid time format. Use 24-hour HH:MM: {time_str}")
        return
    print(f"Starting backup process: src={src}, dst={dst}, interval={interval}, time_str={time_str}")
    stop_event.clear()
    cancel_event.clear()
    set_status("Scheduler running — waiting for next run time…", "blue")
    save_gui_state()
    threading.Thread(target=start_backup, args=(src, dst, interval, time_str), daemon=True).start()


def on_backup_now():
    src = src_entry.get().strip()
    dst = dst_entry.get().strip()
    if not src or not dst:
        messagebox.showerror("Error", "Source and destination folders are required")
        return
    if not os.path.isdir(src):
        messagebox.showerror("Error", "Source folder does not exist or is not a folder")
        return
    save_gui_state()
    cancel_event.clear()

    def progress_cb(done, total):
        root.after(0, lambda d=done, t=total: apply_progress(d, t))

    def work():
        try:
            with copy_lock:
                stats = copy_folder(src, dst, progress_cb=progress_cb, cancel_event=cancel_event)
            root.after(0, lambda s=stats: finish_backup_ui(s, None, scheduled=False))
        except Exception as e:
            root.after(0, lambda err=str(e): finish_backup_ui(None, err, scheduled=False))

    def prepare_and_run():
        begin_manual_backup_ui()
        threading.Thread(target=work, daemon=True).start()

    root.after(0, prepare_and_run)


def on_stop():
    """Cancel any in-progress copy and stop the scheduler loop."""
    cancel_event.set()
    stop_event.set()
    set_status("Stopping…", "darkorange")
    print("Stop requested")


backup_now_btn.configure(command=on_backup_now)
start_backup_btn.configure(command=on_start)
stop_btn.configure(command=on_stop)
# Bring window forward (often hidden behind the IDE when launched from a terminal)
root.update_idletasks()
root.lift()
root.attributes("-topmost", True)
root.after(200, lambda: root.attributes("-topmost", False))


def on_closing():
    stop_event.set()
    cancel_event.set()
    save_gui_state()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
