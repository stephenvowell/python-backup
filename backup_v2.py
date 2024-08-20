import shutil
import os
import filecmp
import logging
import schedule
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import re
import csv

# Ensure the logs directory exists
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging to use the new location
log_file = os.path.join(log_dir, 'copy_errors.csv')
logging.basicConfig(filename=log_file, level=logging.ERROR, 
                    format='%(asctime)s,%(levelname)s,%(message)s', filemode='w')

# Configure a separate logger for successful copies
success_log_file = os.path.join(log_dir, 'copy_success.csv')
success_logger = logging.getLogger('success_logger')
success_handler = logging.FileHandler(success_log_file, mode='w')
success_handler.setLevel(logging.INFO)
success_formatter = logging.Formatter('%(asctime)s,%(message)s')
success_handler.setFormatter(success_formatter)
success_logger.addHandler(success_handler)
success_logger.setLevel(logging.INFO)

# Write headers to the CSV files
with open(log_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'Level', 'Message'])

with open(success_log_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'Message'])

def copy_folder(src, dst):
    print(f"Starting copy from {src} to {dst}")
    if not os.path.exists(dst):
        os.makedirs(dst)
    
    for root, dirs, files in os.walk(src):
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst, os.path.relpath(src_file, src))
            
            try:
                if not os.path.exists(os.path.dirname(dst_file)):
                    os.makedirs(os.path.dirname(dst_file))
                
                if not os.path.exists(dst_file) or not filecmp.cmp(src_file, dst_file, shallow=False):
                    shutil.copy2(src_file, dst_file)
                    print(f"Copied {src_file} to {dst_file}")
                    success_logger.info(f"Copied {src_file} to {dst_file}")
            except Exception as e:
                logging.error(f"Failed to copy {src_file} to {dst_file}: {e}")
                print(f"Error copying {src_file} to {dst_file}: {e}")

def start_backup(src, dst, interval, time_str):
    def job():
        print("Job started")
        copy_folder(src, dst)
        print("Job completed")
    
    # Debugging: Print the time_str to ensure it's correct
    print(f"Scheduling job at {time_str}")
    
    # Validate time format
    if not validate_time_format(time_str):
        logging.error(f"Invalid time format: {time_str}")
        print(f"Invalid time format: {time_str}")
        return
    
    schedule.every(interval).days.at(time_str).do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def browse_folder(entry):
    folder_selected = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, folder_selected)
    print(f"Selected folder: {folder_selected}")

def validate_time_format(time_str):
    # Validate time format HH:MM
    pattern = re.compile(r'^\d{2}:\d{2}$')
    return pattern.match(time_str) is not None

def on_start():
    src = src_entry.get()
    dst = dst_entry.get()
    interval = int(interval_entry.get())
    time_str = time_entry.get()
    
    if not src or not dst or not interval or not time_str:
        messagebox.showerror("Error", "All fields are required")
        print("Error: All fields are required")
        return
    
    if not validate_time_format(time_str):
        messagebox.showerror("Error", "Invalid time format. Use HH:MM")
        print(f"Error: Invalid time format. Use HH:MM: {time_str}")
        return
    
    # Start the backup process in a separate thread
    print(f"Starting backup process: src={src}, dst={dst}, interval={interval}, time_str={time_str}")
    threading.Thread(target=start_backup, args=(src, dst, interval, time_str), daemon=True).start()

# Create the main window
root = tk.Tk()
root.title("Backup Scheduler for Joe")

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

# Time (HH:MM)
tk.Label(root, text="Time (HH:MM):").grid(row=3, column=0, padx=10, pady=5)
time_entry = tk.Entry(root, width=50)
time_entry.grid(row=3, column=1, padx=10, pady=5)

# Start button
tk.Button(root, text="Start Backup", command=on_start).grid(row=4, column=1, pady=20)

root.mainloop()