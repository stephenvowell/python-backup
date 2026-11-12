"""Automate Gumroad zip upload in the default browser via Windows UI."""
import time
from pathlib import Path

import pyautogui
import pyperclip
from pywinauto import Desktop

ZIP = Path(r"C:\Users\Steph\Desktop\PythonBackUp-windows.zip")
if not ZIP.exists():
    ZIP = Path(r"C:\Users\Steph\Projects\PythonBackUp\dist\PythonBackUp-windows.zip")

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.2


def find_gumroad_window():
    for backend in ("uia", "win32"):
        try:
            desktop = Desktop(backend=backend)
            for w in desktop.windows():
                title = w.window_text()
                if title and "Python BackUp" in title and "Gumroad" not in title:
                    return w, backend
                if title and "Gumroad" in title and "BackUp" in title:
                    return w, backend
        except Exception:
            continue
    return None, None


def pick_file_in_dialog(path: str) -> bool:
    time.sleep(1.0)
    for backend in ("uia", "win32"):
        try:
            desktop = Desktop(backend=backend)
            for dlg in desktop.windows():
                t = dlg.window_text() or ""
                if any(x in t for x in ("Open", "File Upload", "Choose File", "Select File")):
                    pyperclip.copy(path)
                    dlg.set_focus()
                    time.sleep(0.3)
                    pyautogui.hotkey("alt", "n")
                    time.sleep(0.2)
                    pyautogui.hotkey("ctrl", "a")
                    pyautogui.hotkey("ctrl", "v")
                    time.sleep(0.2)
                    pyautogui.press("enter")
                    return True
        except Exception:
            continue
    pyperclip.copy(path)
    pyautogui.hotkey("alt", "n")
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    return True


def main() -> None:
    print("Looking for Gumroad window...")
    win, backend = find_gumroad_window()
    if not win:
        titles = []
        for backend in ("uia", "win32"):
            try:
                titles.extend([w.window_text() for w in Desktop(backend=backend).windows() if w.window_text()])
            except Exception:
                pass
        print("Could not find Gumroad window. Visible titles:")
        for t in sorted(set(titles))[:40]:
            print(" ", t)
        raise SystemExit(1)

    print(f"Found window ({backend}): {win.window_text()}")
    win.set_focus()
    time.sleep(0.5)

    # Try keyboard search for upload control
    pyautogui.hotkey("ctrl", "f")
    time.sleep(0.3)
    pyperclip.copy("Upload your files")
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)
    pyautogui.press("escape")
    time.sleep(0.2)

    # Click center-left content area then tab to upload - fragile fallback
    pyautogui.click(700, 500)
    time.sleep(0.3)

    print("Opening upload menu via coordinates near Upload your files...")
    pyautogui.click(430, 430)
    time.sleep(0.8)
    pyautogui.click(430, 500)  # Computer files
    time.sleep(0.5)

    print(f"Selecting file: {ZIP}")
    pick_file_in_dialog(str(ZIP))
    print("Done - check Gumroad page for upload progress")


if __name__ == "__main__":
    main()
