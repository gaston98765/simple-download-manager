# Simple Download Manager (SDM)

## Project Overview

Simple Download Manager (SDM) is a Python-based application inspired by Internet Download Manager (IDM) and Xtreme Download Manager (XDM).

The goal of the project is to improve download speed and reliability using multi-threading and distributed systems concepts.

The application downloads files from URLs and will support segmented downloads, pause/resume, retry mechanisms, progress monitoring, and download history.

---
## Current Implementation
The first implemented module is the core downloader. It supports:
- URL input
- file metadata retrieval
- single-threaded download
- local file saving
- basic start/cancel handling