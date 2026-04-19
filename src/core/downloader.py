import os
import requests

from storage.state_manager import save_state, get_state, delete_state
from utils.retry_handler import retry_request


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

    def _make_request(self, url, headers=None):
        return requests.get(url, stream=True, timeout=15, headers=headers or {})

    def download_file(self, url: str, filename: str, output_folder: str = "downloads") -> str:
        os.makedirs(output_folder, exist_ok=True)
        filepath = os.path.join(output_folder, filename)

        state = get_state(filename)
        downloaded_bytes = 0
        headers = {}
        file_mode = "wb"
        resuming = False

        if state and state.get("url") == url:
            saved_bytes = state.get("downloaded_bytes", 0)
            if saved_bytes > 0 and os.path.exists(filepath):
                downloaded_bytes = saved_bytes
                headers["Range"] = f"bytes={downloaded_bytes}-"
                file_mode = "ab"
                resuming = True
                print(f"Attempting to resume from byte {downloaded_bytes}")

        self.reset_controls()

        response = retry_request(
            lambda: self._make_request(url, headers),
            retries=3,
            delay=2
        )

        with response:
            response.raise_for_status()

            if resuming:
                if response.status_code == 206:
                    print(f"Resuming download from byte {downloaded_bytes}")
                elif response.status_code == 200:
                    print("Server ignored Range header. Restarting from beginning.")
                    downloaded_bytes = 0
                    file_mode = "wb"
                    delete_state(filename)
                    response.close()

                    response = retry_request(
                        lambda: self._make_request(url),
                        retries=3,
                        delay=2
                    )
                else:
                    raise Exception(f"Unexpected status code during resume: {response.status_code}")

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