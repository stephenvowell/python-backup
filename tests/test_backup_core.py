"""Unit tests for backup_core (no GUI required)."""

import os
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import backup_core  # noqa: E402


class TestValidateTimeFormat:
    def test_valid_times(self):
        for t in ["00:00", "09:00", "14:30", "23:59"]:
            assert backup_core.validate_time_format(t) is True

    def test_invalid_times(self):
        for t in ["24:00", "9:00", "14:60", "1430", "", "aa:bb", None, "23:5"]:
            assert backup_core.validate_time_format(t) is False


class TestCopyFolder:
    def test_copies_all_files(self, tmp_path):
        src = tmp_path / "src"
        dst = tmp_path / "dst"
        (src / "sub").mkdir(parents=True)
        (src / "a.txt").write_text("hello")
        (src / "sub" / "b.txt").write_text("world")

        stats = backup_core.copy_folder(str(src), str(dst))

        assert stats["total"] == 2
        assert stats["copied"] == 2
        assert stats["unchanged"] == 0
        assert stats["errors"] == 0
        assert stats["cancelled"] is False
        assert (dst / "a.txt").read_text() == "hello"
        assert (dst / "sub" / "b.txt").read_text() == "world"

    def test_skips_unchanged_on_second_run(self, tmp_path):
        src = tmp_path / "src"
        dst = tmp_path / "dst"
        src.mkdir()
        (src / "a.txt").write_text("hello")

        backup_core.copy_folder(str(src), str(dst))
        stats = backup_core.copy_folder(str(src), str(dst))

        assert stats["copied"] == 0
        assert stats["unchanged"] == 1

    def test_progress_callback_invoked(self, tmp_path):
        src = tmp_path / "src"
        dst = tmp_path / "dst"
        src.mkdir()
        (src / "a.txt").write_text("x")
        (src / "b.txt").write_text("y")

        calls = []
        backup_core.copy_folder(str(src), str(dst), progress_cb=lambda d, t: calls.append((d, t)))

        assert calls[-1] == (2, 2)

    def test_cancel_stops_early(self, tmp_path):
        src = tmp_path / "src"
        dst = tmp_path / "dst"
        src.mkdir()
        for i in range(5):
            (src / f"f{i}.txt").write_text(str(i))

        cancel = threading.Event()
        cancel.set()  # cancel before any work

        stats = backup_core.copy_folder(str(src), str(dst), cancel_event=cancel)

        assert stats["cancelled"] is True
        assert stats["copied"] == 0

    def test_empty_source(self, tmp_path):
        src = tmp_path / "src"
        dst = tmp_path / "dst"
        src.mkdir()

        stats = backup_core.copy_folder(str(src), str(dst))

        assert stats["total"] == 0
        assert stats["copied"] == 0


class TestCsvLogging:
    def test_paths_with_commas_stay_quoted(self, tmp_path, monkeypatch):
        log = tmp_path / "copy_success.csv"
        monkeypatch.setattr(backup_core, "SUCCESS_LOG", str(log))
        monkeypatch.setattr(backup_core, "LOG_DIR", str(tmp_path))

        backup_core.log_success(r"Copied C:\Reports\2024,Q1\a.txt to D:\bak\a.txt")

        import csv

        with open(log, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))

        assert rows[0] == ["Timestamp", "Message"]
        # Message stays in a single column despite the comma in the path.
        assert rows[1][1] == r"Copied C:\Reports\2024,Q1\a.txt to D:\bak\a.txt"

    def test_appends_across_calls(self, tmp_path, monkeypatch):
        log = tmp_path / "copy_success.csv"
        monkeypatch.setattr(backup_core, "SUCCESS_LOG", str(log))
        monkeypatch.setattr(backup_core, "LOG_DIR", str(tmp_path))

        backup_core.log_success("first")
        backup_core.log_success("second")

        import csv

        with open(log, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))

        # Header written once, two data rows appended.
        assert rows[0] == ["Timestamp", "Message"]
        assert rows[1][1] == "first"
        assert rows[2][1] == "second"
