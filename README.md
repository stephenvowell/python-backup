# JoeBackUp

JoeBackUp is a Python-based backup utility that allows users to schedule and manage backups of their files and directories. The application uses a simple graphical user interface (GUI) built with Tkinter.


******* The backupv1.py file has the directions to install the required librarys

## Features

- **Browse and Select Folders**: Easily browse and select source and destination folders for backup.
- **Schedule Backups**: Set the interval (in days) and time (HH:MM) for automated backups.
- **Start Backup**: Initiate the backup process with a single click.

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- Schedule library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/JoeBackUp.git
    cd JoeBackUp
    ```

2. Install the required libraries:
    ```sh
    pip install schedule
    ```

## Usage

1. Run the `backupv1.py` script:
    ```sh
    python backupv1.py
    ```

2. Use the GUI to:
    - Browse and select the source and destination folders.
    - Set the interval (in days) and time (HH:MM) for the backup.
    - Click the "Start Backup" button to begin the backup process.

## Code Overview

### GUI Elements

- **Destination Folder**: 
    ```python
    dst_entry.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_folder(dst_entry)).grid(row=1, column=2, padx=10, pady=5)
    ```

- **Interval (days)**: 
    ```python
    tk.Label(root, text="Interval (days):").grid(row=2, column=0, padx=10, pady=5)
    interval_entry = tk.Entry(root, width=50)
    interval_entry.grid(row=2, column=1, padx=10, pady=5)
    ```

- **Time (HH:MM)**: 
    ```python
    tk.Label(root, text="Time (HH:MM):").grid(row=3, column=0, padx=10, pady=5)
    time_entry = tk.Entry(root, width=50)
    time_entry.grid(row=3, column=1, padx=10, pady=5)
    ```

- **Start Button**: 
    ```python
    tk.Button(root, text="Start Backup", command=on_start).grid(row=4, column=1, pady=20)
    ```

### Main Loop

- **Main Loop**: 
    ```python
    root.mainloop()
    ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
