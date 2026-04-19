from core.file_info import get_file_info
from core.downloader import SimpleDownloader, DownloadCancelled, DownloadPaused
from core.segment_downloader import SegmentDownloader
from core.assembler import merge_files
from utils.progress import ProgressTracker
from storage.history import DownloadHistory
from storage.state_manager import get_state


def main():
    history_manager = DownloadHistory()
    info = None
    url = ""

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

        mode = input("Choose mode: 1 = single-thread, 2 = multi-thread: ").strip()

        if mode == "2" and not info["accept_ranges"]:
            print("Server does not support multi-threaded download. Falling back to single-thread mode.")
            mode = "1"

        if mode == "1":
            saved_state = get_state(info["filename"])
            initial_downloaded = 0

            if saved_state and saved_state.get("url") == info["final_url"]:
                initial_downloaded = saved_state.get("downloaded_bytes", 0)

            tracker = ProgressTracker(
                info["size"] if info["size"] else 0,
                initial_downloaded=initial_downloaded
            )

            downloader = SimpleDownloader()
            saved_path = downloader.download_file(
                info["final_url"],
                info["filename"],
                tracker=tracker
            )

        elif mode == "2":
            num_threads = 4
            downloader = SegmentDownloader(info["final_url"], info["filename"], num_threads)
            downloader.start_download()
            merge_files(info["filename"], num_threads)
            saved_path = f"downloads/{info['filename']}"

        else:
            print("Invalid mode selected.")
            return

        history_manager.add_entry(
            url=info["final_url"],
            filename=info["filename"],
            total_size=info["size"] if info["size"] else 0,
            status="completed"
        )

        print(f"\nDownload complete: {saved_path}")

    except DownloadPaused:
        history_manager.add_entry(
            url=url,
            filename=info["filename"] if info else "unknown",
            total_size=info["size"] if info and info["size"] else 0,
            status="paused"
        )
        print("Download paused.")

    except KeyboardInterrupt:
        history_manager.add_entry(
            url=url,
            filename=info["filename"] if info else "unknown",
            total_size=info["size"] if info and info["size"] else 0,
            status="paused"
        )
        print("\nDownload interrupted with Ctrl+C.")

    except DownloadCancelled as e:
        history_manager.add_entry(
            url=url,
            filename=info["filename"] if info else "unknown",
            total_size=info["size"] if info and info["size"] else 0,
            status="cancelled"
        )
        print(str(e))

    except Exception as e:
        history_manager.add_entry(
            url=url,
            filename=info["filename"] if info else "unknown",
            total_size=info["size"] if info and info["size"] else 0,
            status="failed"
        )
        print(f"Error: {e}")


if __name__ == "__main__":
    main()