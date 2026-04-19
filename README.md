# Simple Download Manager (SDM)

## Project Overview

Simple Download Manager (SDM) is a Python-based application inspired by Internet Download Manager (IDM) and Xtreme Download Manager (XDM).

The goal of this project is to improve file download speed and reliability using multithreading, HTTP Range requests, file handling, and error recovery techniques.

The application supports downloading files from URLs, segmented downloading using threads, pause/resume functionality, retry handling, progress monitoring, and download history.

---

## Objectives

This project demonstrates:

* Multithreading and concurrency
* HTTP Range requests
* File handling
* Error handling and retry logic
* Pause and resume mechanisms
* Progress monitoring
* Persistent download history

---

## Implemented Features

* Download file from URL
* Retrieve file information (name, size, range support)
* Single-threaded download
* Multi-threaded segmented download
* Merge downloaded file parts
* Pause download
* Resume download from saved state
* Retry failed requests automatically
* Progress percentage display
* Download speed calculation
* Estimated remaining time
* Download history storage

---

## Architecture

The project follows a **Layered Architecture**.

**Why this architecture?**
We chose layered architecture because it separates the project into clear modules, making it easier to implement, test, and extend each feature independently.

### Layers

* **UI / Main Layer**
* **Download Manager Core**
* **Thread Controller**
* **Segment Downloader Workers**
* **File Assembler**
* **Persistence Module**

---

## System Components

### `src/main.py`

Entry point of the application.
Handles user interaction and starts the selected download process.

### `src/core/file_info.py`

Retrieves file metadata such as:

* filename
* file size
* range request support

### `src/core/downloader.py`

Handles single-thread downloading and supports:

* pause
* resume
* retry
* progress tracking

### `src/core/segment_downloader.py`

Splits a file into byte segments and downloads them in parallel using threads.

### `src/core/assembler.py`

Merges all downloaded file segments into the final file.

### `src/utils/progress.py`

Tracks:

* downloaded bytes
* progress percentage
* download speed
* estimated remaining time

### `src/utils/retry_handler.py`

Retries failed requests automatically.

### `src/storage/state_manager.py`

Stores and retrieves paused download state.

### `src/storage/history.py`

Stores and displays download history.

---

## Communication Mechanism

The system uses:

* **HTTP requests** to communicate with servers
* **Python function calls** between internal modules
* **threads** for concurrent segmented downloading
* **JSON files** for state persistence and history

---

## Project Structure

```bash
simple-download-manager/
│
├── src/
│   ├── core/
│   │   ├── downloader.py
│   │   ├── segment_downloader.py
│   │   ├── assembler.py
│   │   └── file_info.py
│   │
│   ├── storage/
│   │   ├── history.py
│   │   ├── state_manager.py
│   │   └── data/
│   │       ├── history.json
│   │       └── states.json
│   │
│   ├── utils/
│   │   ├── progress.py
│   │   └── retry_handler.py
│   │
│   └── main.py
│
├── future/   # planned structure
│   ├── manager/
│   │   └── download_manager.py
│   │
│   └── ui/
│       └── cli.py
│
├── downloads/
├── temp/
├── requirements.txt
└── README.md
```

---

## Installation

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
python src/main.py
```

Example test URL:

```text
https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf
```

---

## Team Responsibilities

### Person 1: (gaston98765)

Core download

* URL handling
* file info retrieval
* single-thread download
* file saving
* start/cancel

### Person 2: (safsafa-dev)

Multi-threading

* split file into segments
* parallel download threads
* HTTP Range requests
* merge file parts

### Person 3: (saraTabbane)


Pause / Resume + Retry

* pause download
* resume from last byte
* retry failed requests
* save progress state

### Person 4 : (Louulan)

Progress + History

* progress percentage
* speed calculation
* remaining time
* download history
* active downloads list

---

## Thread Model Explanation

The multi-threaded downloader works by:

1. Retrieving the total file size from the server
2. Dividing the file into byte ranges
3. Creating multiple threads
4. Assigning each thread a specific file segment
5. Downloading all segments concurrently
6. Merging all parts into the final file

This improves speed when the server supports HTTP Range requests.

---

## Challenges Faced

* Handling servers that do not support HTTP Range requests
* Avoiding corrupted files during resume
* Managing progress while downloading in chunks
* Keeping local state and history files clean
* Resolving integration conflicts between multiple modules

---

## Performance Comparison

A single-threaded download retrieves the file sequentially.
A multi-threaded download splits the file into multiple parts and downloads them at the same time.

In general, multi-threading can improve performance when:

* the server supports range requests
* the network connection allows parallel transfers

---

## Future Improvements

* Better CLI menu
* Full integration of progress with segmented downloads
* Active downloads dashboard
* Download scheduling
* Bandwidth limiting
* Graphical user interface (GUI)
* Better cancellation handling with Ctrl+C
