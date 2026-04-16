import os
import threading
import requests


class SegmentDownloader:
    def __init__(self, url, output_name, num_threads=4):
        self.url = url
        self.output_name = output_name
        self.num_threads = num_threads
        self.temp_folder = "temp"

        os.makedirs(self.temp_folder, exist_ok=True)

    def get_file_size(self):
        response = requests.head(self.url)
        return int(response.headers.get("Content-Length", 0))

    def download_segment(self, start, end, part_num):
        headers = {"Range": f"bytes={start}-{end}"}

        response = requests.get(self.url, headers=headers, stream=True)

        part_path = os.path.join(self.temp_folder, f"part{part_num}")

        with open(part_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

        print(f"Segment {part_num} finished")

    def start_download(self):
        file_size = self.get_file_size()
        part_size = file_size // self.num_threads

        threads = []

        for i in range(self.num_threads):
            start = i * part_size

            if i == self.num_threads - 1:
                end = file_size - 1
            else:
                end = start + part_size - 1

            thread = threading.Thread(
                target=self.download_segment,
                args=(start, end, i)
            )

            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print("All segments downloaded")
