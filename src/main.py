from core.file_info import get_file_info
from core.downloader import SimpleDownloader, DownloadCancelled
from utils.progress import ProgressTracker
from storage.history import DownloadHistory


def main():
    history_manager = DownloadHistory()

    show_history = input("Do you want to see download history? (y/n): ").strip().lower()
    if show_history == "y":
        history_manager.show_history()

    url = input("\nEnter file URL: ").strip()

    if not url:
        print("URL cannot be empty.")
        return

    try:
        info = get_file_info(url)

        print("\nFile information:")
        print(f"Name: {info['filename']}")
        print(f"Size: {info['size']} bytes" if info["size"] else "Size: Unknown")
        print(f"Range support: {info['accept_ranges']}")

        start = input("\nStart download? (y/n): ").strip().lower()
        if start != "y":
            print("Download cancelled before start.")
            return

        tracker = ProgressTracker(info["size"] if info["size"] else 0)

        downloader = SimpleDownloader()
        saved_path = downloader.download_file(
            info["final_url"],
            info["filename"],
            tracker=tracker
        )

        history_manager.add_entry(
            url=info["final_url"],
            filename=info["filename"],
            total_size=info["size"] if info["size"] else 0,
            status="completed"
        )

        print(f"\nDownload complete: {saved_path}")

    except DownloadCancelled as e:
        history_manager.add_entry(
            url=url,
            filename="unknown",
            total_size=0,
            status="cancelled"
        )
        print(str(e))

    except Exception as e:
        history_manager.add_entry(
            url=url,
            filename="unknown",
            total_size=0,
            status="failed"
        )
        print(f"Error: {e}")


if __name__ == "__main__":
    main()