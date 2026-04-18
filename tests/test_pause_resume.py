import sys
import os
import threading
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.downloader import SimpleDownloader, DownloadPaused, DownloadCancelled

URL = "http://ipv4.download.thinkbroadband.com/20MB.zip"
FILENAME = "test_file.zip"

downloader = SimpleDownloader()


def start_download():
    try:
        print("Starting download...")
        path = downloader.download_file(URL, FILENAME)
        print(f"Download finished successfully: {path}")

    except DownloadPaused:
        print("Download paused successfully!")

    except DownloadCancelled:
        print("Download cancelled!")

    except Exception as e:
        print("Error:", e)


thread = threading.Thread(target=start_download)
thread.start()

# Wait a little, then pause the download
time.sleep(3)
#downloader.pause()

thread.join()

print("\nRun the same file again to test resume.")