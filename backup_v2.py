import os
import time
import json
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import schedule

from backup_core import copy_folder, validate_time_format, log_error, LOG_DIR, app_dir
from version import __version__
from backup_theme import (
    ACCENT,
    ACCENT_H,
    ACCENT_L,
    BG,
    CONSOLE_BG,
    DANGER,
    DANGER_H,
    FONT,
    MONO,
    MUTED,
    OK,
    PANEL,
    PANEL2,
    TEXT,
    WARN,
)

os.makedirs(LOG_DIR, exist_ok=True)

copy_lock = threading.Lock()
cancel_event = threading.Event()
stop_event = threading.Event()
_scheduler_thread = None

_log_queue = []
_log_flush_pending = False

_STATE_FILE = os.path.join(app_dir(), "gui_state.json")


def _btn(parent, text, command, *, base=ACCENT, hover=ACCENT_H, secondary=False):
    if secondary:
        base, hover = PANEL2, PANEL
    b = tk.Button(
        parent,
        text=text,
        command=command,
        bg=base,
        fg="#ffffff",
        activebackground=hover,
        activeforeground="#ffffff",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=(FONT, 10, "bold"),
        padx=12,
        pady=6,
    )
    b.bind(
        "<Enter>",
        lambda _e: b.configure(bg=hover) if str(b["state"]) != "disabled" else None,
    )
    b.bind(
        "<Leave>",
        lambda _e: b.configure(bg=base) if str(b["state"]) != "disabled" else None,
    )
    b._base = base  # type: ignore[attr-defined]
    return b


def _label(parent, text=None, **kwargs):
    opts = {"bg": BG, "fg": TEXT, "font": (FONT, 10), **kwargs}
    if text is not None:
        opts["text"] = text
    return tk.Label(parent, **opts)


def _entry(parent, width=50):
    return tk.Entry(
        parent,
        width=width,
        bg=PANEL,
        fg=TEXT,
        insertbackground=ACCENT_L,
        relief="flat",
        font=(FONT, 10),
        disabledbackground=PANEL,
    )


def _configure_ttk(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure(
        "Backup.Horizontal.TProgressbar",
        troughcolor=PANEL2,
        background=ACCENT,
        bordercolor=PANEL,
        lightcolor=ACCENT,
        darkcolor=ACCENT,
        thickness=10,
    )


root = tk.Tk()
root.title(f"Python BackUp v{__version__}")
root.configure(bg=BG)
root.geometry("720x680")
root.minsize(600, 520)
_configure_ttk(root)

pad = {"padx": 22, "pady": 6}
form = tk.Frame(root, bg=BG)
form.pack(fill="x", padx=0, pady=(18, 8))

header = tk.Frame(form, bg=BG)
header.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 10))
tk.Label(header, text="Python BackUp", bg=BG, fg=TEXT, font=(FONT, 20, "bold")).pack(
    side="left"
)
tk.Label(
    header,
    text=f"v{__version__} · Scheduled folder sync",
    bg=BG,
    fg=MUTED,
    font=(FONT, 10, "italic"),
).pack(side="right")

_label(form, text="Source Folder:").grid(row=1, column=0, sticky="w", **pad)
src_entry = _entry(form)
src_entry.grid(row=1, column=1, sticky="ew", **pad)
_btn(form, "Browse", lambda: browse_folder(src_entry), secondary=True).grid(
    row=1, column=2, **pad
)

_label(form, text="Destination Folder:").grid(row=2, column=0, sticky="w", **pad)
dst_entry = _entry(form)
dst_entry.grid(row=2, column=1, sticky="ew", **pad)
_btn(form, "Browse", lambda: browse_folder(dst_entry), secondary=True).grid(
    row=2, column=2, **pad
)

_label(form, text="Interval (days):").grid(row=3, column=0, sticky="w", **pad)
interval_entry = _entry(form)
interval_entry.grid(row=3, column=1, sticky="ew", **pad)

_label(form, text="Time (24-hour HH:MM):").grid(row=4, column=0, sticky="w", **pad)
time_entry = _entry(form)
time_entry.grid(row=4, column=1, sticky="ew", **pad)

progress_var = tk.DoubleVar(value=0)
progress_bar = ttk.Progressbar(
    form,
    variable=progress_var,
    maximum=100,
    mode="determinate",
    length=400,
    style="Backup.Horizontal.TProgressbar",
)
progress_bar.grid(row=5, column=0, columnspan=3, padx=22, pady=(12, 4), sticky="ew")

status_var = tk.StringVar(value="Ready")
status_label = _label(form, textvariable=status_var, anchor="w", fg=MUTED)
status_label.grid(row=6, column=0, columnspan=3, padx=22, pady=(0, 8), sticky="ew")

btn_row = tk.Frame(form, bg=BG)
btn_row.grid(row=7, column=0, columnspan=3, pady=(4, 4))
backup_now_btn = _btn(btn_row, "Backup Now", None)
start_backup_btn = _btn(btn_row, "Start Backup", None)
stop_btn = _btn(btn_row, "Stop", None, base=DANGER, hover=DANGER_H)
backup_now_btn.pack(side=tk.LEFT, padx=(0, 8))
start_backup_btn.pack(side=tk.LEFT, padx=(0, 8))
stop_btn.pack(side=tk.LEFT, padx=(0, 8))
clear_log_btn = _btn(btn_row, "Clear log", None, secondary=True)
clear_log_btn.pack(side=tk.LEFT)

form.columnconfigure(1, weight=1)

console_wrap = tk.Frame(root, bg=ACCENT)
console_wrap.pack(fill="both", expand=True, padx=22, pady=(0, 18))
console = tk.Text(
    console_wrap,
    bg=CONSOLE_BG,
    fg=TEXT,
    insertbackground=ACCENT_L,
    font=(MONO, 9),
    relief="flat",
    bd=0,
    wrap="none",
    padx=10,
    pady=8,
    state="disabled",
    height=14,
)
console.grid(row=0, column=0, sticky="nsew")
console_scroll = tk.Scrollbar(console_wrap, command=console.yview)
console_scroll.grid(row=0, column=1, sticky="ns")
console_xscroll = tk.Scrollbar(console_wrap, orient="horizontal", command=console.xview)
console_xscroll.grid(row=1, column=0, sticky="ew")
console.configure(yscrollcommand=console_scroll.set, xscrollcommand=console_xscroll.set)
console_wrap.rowconfigure(0, weight=1)
console_wrap.columnconfigure(0, weight=1)
console.tag_configure("sys", foreground=MUTED, font=(MONO, 9, "italic"))
console.tag_configure("ok", foreground=OK)
console.tag_configure("skip", foreground=MUTED)
console.tag_configure("err", foreground=DANGER)


def ui_log(text, tag=None):
    """Append to the live log (batched so large backups stay responsive)."""
    print(text, end="" if text.endswith("\n") else "\n")
    _log_queue.append((text, tag))
    try:
        root.after(0, _maybe_start_flush)
    except tk.TclError:
        pass


def _maybe_start_flush():
    global _log_flush_pending
    if _log_flush_pending:
        return
    _log_flush_pending = True
    _flush_log_queue()


def _flush_log_queue():
    global _log_flush_pending
    if not _log_queue:
        _log_flush_pending = False
        return
    chunk = _log_queue[:250]
    del _log_queue[:250]
    console.configure(state="normal")
    for text, tag in chunk:
        if tag:
            console.insert("end", text, tag)
        else:
            console.insert("end", text)
    console.see("end")
    console.configure(state="disabled")
    if _log_queue:
        root.after(50, _flush_log_queue)
    else:
        _log_flush_pending = False


def clear_log():
    global _log_flush_pending
    _log_queue.clear()
    _log_flush_pending = False
    console.configure(state="normal")
    console.delete("1.0", "end")
    console.configure(state="disabled")


def log_cb(message, tag=None):
    ui_log(message, tag)


def start_backup(src, dst, interval, time_str):
    def job():
        ui_log("\n--- Scheduled backup started ---\n", "sys")
        cancel_event.clear()
        ready = threading.Event()

        def ping_ui():
            set_status("Running scheduled backup…", ACCENT_L)
            progress_bar.configure(maximum=100)
            progress_var.set(0)
            ready.set()

        root.after(0, ping_ui)
        if not ready.wait(timeout=30):
            log_error("Scheduled backup: UI did not respond in time")
            ui_log("Scheduled backup: UI ping timed out\n", "err")
            return

        def progress_cb(done, total):
            throttled_progress(done, total)

        try:
            with copy_lock:
                stats = copy_folder(
                    src,
                    dst,
                    progress_cb=progress_cb,
                    log_cb=log_cb,
                    cancel_event=cancel_event,
                )
            root.after(0, lambda s=stats: finish_backup_ui(s, None, scheduled=True))
        except Exception as e:
            root.after(0, lambda err=str(e): finish_backup_ui(None, err, scheduled=True))
        ui_log("--- Scheduled backup finished ---\n", "sys")

    schedule.clear()
    ui_log(f"Scheduler armed — every {interval} day(s) at {time_str}\n", "sys")
    if not validate_time_format(time_str):
        log_error(f"Invalid time format: {time_str}")
        ui_log(f"Invalid time format: {time_str}\n", "err")
        return
    schedule.every(interval).days.at(time_str).do(job)
    while not stop_event.is_set():
        schedule.run_pending()
        time.sleep(1)
    schedule.clear()
    ui_log("Scheduler stopped.\n", "sys")


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
    ui_log(f"Selected folder: {folder_selected}\n", "sys")
    save_gui_state()


load_gui_state()
ui_log("Ready. Choose folders and click Backup Now, or Start Backup for a schedule.\n", "sys")


def apply_progress(done, total):
    if total <= 0:
        progress_bar.configure(maximum=1)
        progress_var.set(1)
    else:
        progress_bar.configure(maximum=total)
        progress_var.set(done)


_last_progress = {"done": -1}


def throttled_progress(done, total):
    """Update the bar often enough to feel live without flooding Tk."""
    if total <= 0:
        root.after(0, lambda: apply_progress(done, total))
        return
    step = max(1, total // 200)
    if done == total or done == 1 or done - _last_progress["done"] >= step:
        _last_progress["done"] = done
        root.after(0, lambda d=done, t=total: apply_progress(d, t))


def set_status(text, color=MUTED):
    status_var.set(text)
    status_label.configure(fg=color)


def _set_btn_enabled(btn, enabled):
    if enabled:
        btn.configure(state=tk.NORMAL, bg=btn._base)
    else:
        btn.configure(state=tk.DISABLED, bg=PANEL)


def begin_manual_backup_ui():
    clear_log()
    _last_progress["done"] = -1
    set_status("Copying…", ACCENT_L)
    progress_bar.configure(maximum=100)
    progress_var.set(0)
    _set_btn_enabled(backup_now_btn, False)
    ui_log("Backup Now started…\n", "sys")


def finish_backup_ui(stats, err, scheduled=False):
    _set_btn_enabled(backup_now_btn, True)
    if err:
        apply_progress(0, 1)
        progress_var.set(0)
        set_status(f"Failed: {err}", DANGER)
        ui_log(f"Failed: {err}\n", "err")
        messagebox.showerror("Backup", f"Backup failed:\n{err}")
        return
    if stats.get("cancelled"):
        set_status(
            f"Stopped — {stats['copied']} copied, {stats['unchanged']} unchanged before cancel.",
            WARN,
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
        set_status(msg, OK)
    else:
        msg = (
            f"Finished with {stats['errors']} error(s). "
            f"{stats['copied']} copied, {stats['unchanged']} unchanged. See logs."
        )
        set_status(msg, DANGER)
        title = "Scheduled backup" if scheduled else "Backup"
        messagebox.showwarning(title, msg)


def on_start():
    global _scheduler_thread
    if _scheduler_thread is not None and _scheduler_thread.is_alive():
        messagebox.showinfo("Scheduler", "A backup schedule is already running.")
        return
    src = src_entry.get()
    dst = dst_entry.get()
    interval_raw = interval_entry.get()
    time_str = time_entry.get()
    if not src or not dst or not interval_raw or not time_str:
        messagebox.showerror("Error", "All fields are required")
        ui_log("Error: All fields are required\n", "err")
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
        ui_log(f"Error: Invalid time format: {time_str}\n", "err")
        return
    ui_log(
        f"Starting scheduler: src={src}, dst={dst}, every {interval} day(s) at {time_str}\n",
        "sys",
    )
    stop_event.clear()
    cancel_event.clear()
    set_status("Scheduler running — waiting for next run time…", ACCENT_L)
    save_gui_state()
    _set_btn_enabled(start_backup_btn, False)
    _scheduler_thread = threading.Thread(
        target=start_backup, args=(src, dst, interval, time_str), daemon=True
    )
    _scheduler_thread.start()


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
        throttled_progress(done, total)

    def work():
        try:
            with copy_lock:
                stats = copy_folder(
                    src,
                    dst,
                    progress_cb=progress_cb,
                    log_cb=log_cb,
                    cancel_event=cancel_event,
                )
            root.after(0, lambda s=stats: finish_backup_ui(s, None, scheduled=False))
        except Exception as e:
            root.after(0, lambda err=str(e): finish_backup_ui(None, err, scheduled=False))

    def prepare_and_run():
        begin_manual_backup_ui()
        threading.Thread(target=work, daemon=True).start()

    root.after(0, prepare_and_run)


def on_clear_log():
    clear_log()
    ui_log("Log cleared.\n", "sys")


def on_stop():
    cancel_event.set()
    stop_event.set()
    schedule.clear()
    set_status("Stopping…", WARN)
    ui_log("Stop requested.\n", "sys")
    _set_btn_enabled(start_backup_btn, True)


backup_now_btn.configure(command=on_backup_now)
start_backup_btn.configure(command=on_start)
stop_btn.configure(command=on_stop)
clear_log_btn.configure(command=on_clear_log)

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
