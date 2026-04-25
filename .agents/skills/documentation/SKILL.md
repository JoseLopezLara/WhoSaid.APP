---
name: documentation
description:
  Use this skill to access official documentation for core libraries (YouTube API, NLTK) and Python coding standards used in the project.
---

# Documentation Skill

Consult these sources before implementing new library-specific logic or troubleshooting library errors.

## Core Libraries
- **yt-dlp**: [https://github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
    - **Primary tool** for transcript extraction.
    - Check for: Audio extraction, client spoofing (`player_client`), and format selection (`json3`).
- **YouTube Transcript API**: [https://github.com/jdepoix/youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
    - *Deprecated in this project* due to aggressive IP blocking.
- **NLTK (Natural Language Toolkit)**: [https://www.nltk.org/](https://www.nltk.org/)
    - Check for: Stopwords corpus availability and tokenization alternatives.
- **Concurrent Futures (Python StdLib)**: [https://docs.python.org/3/library/concurrent.futures.html](https://docs.python.org/3/library/concurrent.futures.html)
    - Check for: ThreadPoolExecutor vs ProcessPoolExecutor usage.

## Python Packaging
- **SetupTools / PyProject**: [https://setuptools.pypa.io/en/latest/userguide/quickstart.html](https://setuptools.pypa.io/en/latest/userguide/quickstart.html)
    - Check for: Proper `setup.py` structure for local installation via `pip install -e .`.

## General Standards
- **PEP 8**: [https://peps.python.org/pep-0008/](https://peps.python.org/pep-0008/)
    - Coding style and naming conventions.
