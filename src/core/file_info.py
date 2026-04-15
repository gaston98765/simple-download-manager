import requests
from urllib.parse import urlparse, unquote
import os


def get_file_info(url: str) -> dict:
    """
    Fetch basic file info from the server using a HEAD request.
    Returns filename, size, and whether range requests are supported.
    """
    response = requests.head(url, allow_redirects=True, timeout=10)
    response.raise_for_status()

    content_length = response.headers.get("Content-Length")
    accept_ranges = response.headers.get("Accept-Ranges", "").lower() == "bytes"

    filename = None

    content_disposition = response.headers.get("Content-Disposition")
    if content_disposition and "filename=" in content_disposition:
        filename = content_disposition.split("filename=")[-1].strip('"')

    if not filename:
        parsed = urlparse(response.url)
        filename = os.path.basename(parsed.path)

    if not filename:
        filename = "downloaded_file"

    return {
        "filename": unquote(filename),
        "size": int(content_length) if content_length else None,
        "accept_ranges": accept_ranges,
        "final_url": response.url,
    }