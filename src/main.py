from core.file_info import get_file_info
from core.downloader import SimpleDownloader, DownloadCancelled


def main():
    url = input("Enter file URL: ").strip()

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

        downloader = SimpleDownloader()
        saved_path = downloader.download_file(info["final_url"], info["filename"])

        print(f"\nDownload complete: {saved_path}")

    except DownloadCancelled as e:
        print(str(e))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()