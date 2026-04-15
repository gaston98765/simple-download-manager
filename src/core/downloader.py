import os
import requests


class DownloadCancelled(Exception):
    pass


class SimpleDownloader:
    def __init__(self):
        self.cancelled = False

    def cancel(self):
        self.cancelled = True

    def download_file(self, url: str, filename: str, output_folder: str = "downloads") -> str:
        """
        Download a file using a single thread and save it to disk.
        """
        os.makedirs(output_folder, exist_ok=True)
        filepath = os.path.join(output_folder, filename)

        with requests.get(url, stream=True, timeout=15) as response:
            response.raise_for_status()

            with open(filepath, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if self.cancelled:
                        if os.path.exists(filepath):
                            os.remove(filepath)
                        raise DownloadCancelled("Download was cancelled.")

                    if chunk:
                        file.write(chunk)

        return filepath