import os
import threading
import requests


class SegmentDownloader:
    def __init__(self, url, output_name, num_threads=4):
        self.url = url
        self.output_name = output_name
        self.num_threads = num_threads
        self.temp_folder = "temp"
        self.errors = []

        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder)

    def get_file_info(self):
        response = requests.head(self.url, timeout=5)
        response.raise_for_status()

        file_size = int(response.headers.get("Content-Length", 0))
        accept_ranges = response.headers.get("Accept-Ranges", "")

        if accept_ranges.lower() != "bytes":
            raise Exception("Server does not support range requests")

        return file_size

    def download_segment(self, start, end, part_num):
        headers = {"Range": f"bytes={start}-{end}"}

        try:
            response = requests.get(
                self.url,
                headers=headers,
                stream=True,
                timeout=5
            )

            response.raise_for_status()

            if response.status_code != 206:
                raise Exception(f"Expected 206 Partial Content, got {response.status_code}")

            part_path = os.path.join(
                self.temp_folder,
                f"{self.output_name}.part{part_num}"
            )

            with open(part_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

            print(f"[✓] Segment {part_num} finished")

        except Exception as e:
            print(f"[✗] Segment {part_num} failed: {e}")
            self.errors.append(part_num)

    def start_download(self):
        file_size = self.get_file_info()
        part_size = file_size // self.num_threads

        threads = []

        for i in range(self.num_threads):
            start = i * part_size

            if i == self.num_threads - 1:
                end = file_size - 1
            else:
                end = (start + part_size - 1)

            thread = threading.Thread(
                target=self.download_segment,
                args=(start, end, i)
            )

            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        if self.errors:
            raise Exception(f"Download failed. Missing segments: {self.errors}")

        print("[✓] All segments downloaded successfully")
