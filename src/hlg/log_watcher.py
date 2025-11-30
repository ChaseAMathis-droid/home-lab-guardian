"""Log file watcher using watchdog"""

import time
from pathlib import Path
from typing import Generator

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


class LogTailer(FileSystemEventHandler):
    """Tail a log file and yield new lines"""

    def __init__(self, log_path: str):
        self.log_path = Path(log_path)
        self.file_handle = None
        self.position = 0

    def start(self) -> None:
        """Open the log file and seek to the end"""
        if not self.log_path.exists():
            raise FileNotFoundError(f"Log file not found: {self.log_path}")

        self.file_handle = open(self.log_path, "r")
        # Seek to end of file
        self.file_handle.seek(0, 2)
        self.position = self.file_handle.tell()

    def read_new_lines(self) -> Generator[str, None, None]:
        """Read and yield new lines from the log file"""
        if not self.file_handle:
            return

        # Check if file was truncated (rotated)
        current_size = self.log_path.stat().st_size
        if current_size < self.position:
            self.file_handle.seek(0)
            self.position = 0

        self.file_handle.seek(self.position)
        for line in self.file_handle:
            yield line.rstrip("\n")
        self.position = self.file_handle.tell()

    def close(self) -> None:
        """Close the log file"""
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None


def watch_log_file(log_path: str, poll_interval: int = 1) -> Generator[str, None, None]:
    """
    Watch a log file and yield new lines as they appear

    Args:
        log_path: Path to the log file to watch
        poll_interval: How often to check for new lines (seconds)

    Yields:
        New lines from the log file
    """
    tailer = LogTailer(log_path)
    tailer.start()

    try:
        while True:
            for line in tailer.read_new_lines():
                yield line
            time.sleep(poll_interval)
    finally:
        tailer.close()
