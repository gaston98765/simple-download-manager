from src.core.segment_downloader import SegmentDownloader
from src.core.assembler import merge_files

url = "http://ipv4.download.thinkbroadband.com/50MB.zip"

downloader = SegmentDownloader(url, "test.bin", 4)
downloader.start_download()

merge_files("test.bin", 4)
