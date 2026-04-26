---
name: business-logic
description:
  Use this skill to consult business rules, data processing logic for N-grams (Union/Intersection), and the resulting file structure.
---

# Business Logic Skill

This document details the functionality, business rules, and data structure of the YouTube phrase (N-gram) extraction and analysis tool.

## Objective
The tool identifies recurring phrases (from 2 to 6 words) in videos from specific content creators. It uses parallel processing for transcript downloads and statistical analysis, allowing a distinction between popular phrases (Union) and characteristic phrases that appear in most of their videos (Intersection).

## Inputs
The tool receives a Python dictionary where the Key is the YouTube video URL and the Value is the creator's name.
Example:
```python
{
    "https://www.youtube.com/watch?v=vId1": "CREATOR_A",
    "https://www.youtube.com/watch?v=vId2": "CREATOR_B"
}
```

## Business Rules and Functionality

### Stage 1: Download (Evasion-Focused)
- **ID Extraction**: URLs are parsed to extract the 11-character video ID.
- **Engine**: Uses `yt-dlp` instead of standard APIs to mimic human browser behavior.
- **Evasion Techniques**:
    - **Client Spoofing**: Mimics Android and Web clients to bypass "Proof of Origin" tokens.
    - **User-Agent Rotation**: Uses modern browser headers.
    - **Human-like Delays**: Implements random delays (90-120s) between requests to ensure service continuity.
- **Languages**: Attempts to fetch the transcript in Spanish (`es`) first, falling back to English (`en`) if unavailable.
- **Format**: Extracts and parses the `json3` YouTube format.
- **Persistence**: Saves raw data (transcript + metadata) into individual JSON files per video.

### Stage 2: Processing
- **Text Cleaning**: Converts text to lowercase and removes punctuation marks.
- **Tokenization with Timestamps (Multi-block Handling)**: The tool decomposes the full transcript into a flat list of words (tokens). Each token retains the start and end time from its original block. This allows an N-gram to be formed by words belonging to different text blocks fluently.
- **Temporal Continuity**: When generating an N-gram that crosses blocks, the start time is taken from the first token of the N-gram and the end time from the last token, ensuring precision in the phrase's timestamp.
- **N-gram Generation**: Generates combinations of consecutive words (size controlled by `MIN_GRAM_SIZE` and `MAX_GRAM_SIZE` in `config/analysis.py`).
- **Stopwords Filter**: An N-gram is discarded ONLY if ALL the words composing it are stopwords (e.g., "of the"). If it contains at least one semantic word, it is kept.
- **Analysis Metrics**:
    - **Union**: Represents the absolute frequency of the phrase across the entire video set.
    - **Intersection**: Phrases that appear in a percentage equal to or greater than the `INTERSECTION_THRESHOLD` of the total videos processed for that creator.
- **Output Modes**:
    - `first_appearance`: Records the first occurrence of the phrase and the total number of repetitions.
    - `all_appearances`: Records every single time the phrase was spoken, including its URL and specific timestamp.

## File Structure (Output)

The project generates a folder hierarchy under `processed_files/`:

```text
processed_files/
├── processed_transcriptions/          # Raw transcripts by creator
│   ├── CREATOR_A/
│   │   ├── videoId1.json
│   │   └── videoId2.json
│   └── CREATOR_B/
│       └── ...
└── processed_n_gramas/                # Analysis results
    ├── creators/                      # Individual results
    │   ├── CREATOR_A/
    │   │   ├── all_appearances/       # Detail of every appearance
    │   │   │   ├── n_gramas_interception.json
    │   │   │   └── n_gramas_union.json
    │   │   └── first_appearance/      # Summary (first appearance)
    │   │       ├── n_gramas_interception.json
    │   │       └── n_gramas_union.json
    │   └── CREATOR_B/
    │       └── ...
    └── global/                        # Aggregated data for all creators
        ├── all_appearances/
        │   ├── n_gramas_interception.json
        │   └── n_gramas_union.json
        └── first_appearance/
            ├── n_gramas_interception.json
            └── n_gramas_union.json
```

## Data Format (JSON)

### n_gramas_union.json (Example: `first_appearance`)
```json
{
  "2_grams": [
    {
      "phrase": "hello there",
      "repetitions": 15,
      "first_appearance": {
        "start": 10.5,
        "end": 12.0,
        "url": "..."
      }
    }
  ]
}
```
