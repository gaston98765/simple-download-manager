import time
import threading


def format_bytes(num_bytes: float) -> str:
    if num_bytes < 1024:
        return f"{num_bytes:.2f} B"
    elif num_bytes < 1024 ** 2:
        return f"{num_bytes / 1024:.2f} KB"
    elif num_bytes < 1024 ** 3:
        return f"{num_bytes / (1024 ** 2):.2f} MB"
    return f"{num_bytes / (1024 ** 3):.2f} GB"


def format_time(seconds: float | None) -> str:
    if seconds is None:
        return "calculating..."
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"


class ProgressTracker:
    def __init__(self, total_size: int):
        self.total_size = total_size
        self.downloaded = 0
        self.start_time = time.time()
        self.lock = threading.Lock()

    def update(self, chunk_size: int) -> None:
        with self.lock:
            self.downloaded += chunk_size

    def get_downloaded(self) -> int:
        with self.lock:
            return self.downloaded

    def get_percentage(self) -> float:
        with self.lock:
            if self.total_size <= 0:
                return 0.0
            return (self.downloaded / self.total_size) * 100

    def get_speed(self) -> float:
        with self.lock:
            elapsed = time.time() - self.start_time
            if elapsed <= 0:
                return 0.0
            return self.downloaded / elapsed

    def get_remaining_time(self) -> float | None:
        speed = self.get_speed()
        if speed <= 0:
            return None
        with self.lock:
            remaining = self.total_size - self.downloaded
        if remaining < 0:
            remaining = 0
        return remaining / speed

    def get_status_line(self) -> str:
        downloaded = self.get_downloaded()
        percentage = self.get_percentage()
        speed = self.get_speed()
        eta = self.get_remaining_time()

        return (
            f"{percentage:.2f}% | "
            f"{format_bytes(downloaded)} / {format_bytes(self.total_size)} | "
            f"{format_bytes(speed)}/s | "
            f"ETA: {format_time(eta)}"
        )