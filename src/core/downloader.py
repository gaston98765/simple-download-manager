import os
import requests

from src.storage.state_manager import save_state, get_state, delete_state
from src.utils.retry_handler import retry_request


class DownloadCancelled(Exception):
    pass


class DownloadPaused(Exception):
    pass


class SimpleDownloader:
    def __init__(self):
        self.cancelled = False
        self.paused = False

    def cancel(self):
        self.cancelled = True

    def pause(self):
        self.paused = True

    def reset_controls(self):
        self.cancelled = False
        self.paused = False

    def download_file(self, url: str, filename: str, output_folder: str = "downloads") -> str:
        """
        Download a file using a single thread and save it to disk.
        Supports pause, resume, and retry.
        """
        os.makedirs(output_folder, exist_ok=True)
        filepath = os.path.join(output_folder, filename)

        state = get_state(filename)
        downloaded_bytes = 0
        headers = {}
        file_mode = "wb"

        if state and state.get("url") == url:
            downloaded_bytes = state.get("downloaded_bytes", 0)

            if downloaded_bytes > 0 and os.path.exists(filepath):
                headers["Range"] = f"bytes={downloaded_bytes}-"
                file_mode = "ab"
                print(f"Resuming download from byte {downloaded_bytes}")

        self.reset_controls()

        def make_request():
            return requests.get(url, stream=True, timeout=15, headers=headers)

        response = retry_request(make_request, retries=3, delay=2)

        with response:
            response.raise_for_status()

            with open(filepath, file_mode) as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if self.cancelled:
                        if os.path.exists(filepath):
                            os.remove(filepath)
                        delete_state(filename)
                        raise DownloadCancelled("Download was cancelled.")

                    if self.paused:
                        save_state(filename, {
                            "url": url,
                            "downloaded_bytes": downloaded_bytes
                        })
                        raise DownloadPaused("Download was paused.")

                    if chunk:
                        file.write(chunk)
                        downloaded_bytes += len(chunk)

                        save_state(filename, {
                            "url": url,
                            "downloaded_bytes": downloaded_bytes
                        })

        delete_state(filename)
        return filepath