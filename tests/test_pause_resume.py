import sys
import os
import threading
import time

# Add src folder to Python path so we can import core/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from core.downloader import SimpleDownloader, DownloadPaused, DownloadCancelled

# Test file (safe HTTP source)
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


# Run download in separate thread so we can pause it
thread = threading.Thread(target=start_download)
thread.start()

# Wait a few seconds, then pause
time.sleep(3)
downloader.pause()

# Wait for thread to finish
thread.join()

print("\nRun the same file again to test resume.")