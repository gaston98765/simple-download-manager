import json
import os
from datetime import datetime


class DownloadHistory:
    def __init__(self, file_path: str = "src/storage/data/history.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load_history(self) -> list:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_history(self, history: list) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

    def add_entry(
        self,
        url: str,
        filename: str,
        total_size: int,
        status: str,
    ) -> None:
        history = self.load_history()
        history.append(
            {
                "url": url,
                "filename": filename,
                "total_size": total_size,
                "status": status,
                "downloaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        self.save_history(history)

    def show_history(self) -> None:
        history = self.load_history()
        if not history:
            print("No download history found.")
            return

        print("\nDownload History:")
        for i, entry in enumerate(history, start=1):
            print(
                f"{i}. {entry['filename']} | "
                f"{entry['status']} | "
                f"{entry['downloaded_at']}"
            )