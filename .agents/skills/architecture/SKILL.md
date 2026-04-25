---
name: architecture
description:
  Use this skill to understand the project's modular architecture, component responsibilities, and protocols for extending functionality.
---

# Architecture Skill

This guide explains the technical structure of WhoSaid.APP and how to extend its functionality.

## Modular OOP Design
The system is divided into independent modules within `src/whosaid/`.

### Component Map
- **TranscriptDownloader (`downloader.py`)**: Responsible ONLY for fetching data from YouTube API.
- **TextProcessor (`processor.py`)**: Responsible ONLY for text cleaning and multi-block tokenization.
- **NgramAnalyzer (`analyzer.py`)**: Orchestrates the processor to generate statistical insights.
- **StorageManager (`storage.py`)**: Handles the file system hierarchy and JSON persistence.

## Extension Protocol: Adding New Features
To add a new functionality (e.g., Sentiment Analysis), follow these steps:

1. **Create the Logic**: Add a new module in `src/whosaid/sentiment.py`.
2. **Expose the Class**: Add the new class to `src/whosaid/__init__.py`.
3. **Integration**: If it's a processing step, integrate it into `NgramAnalyzer` or create a new orchestrator.
4. **Update Notebook**: Reference the new class in `youtube_ngrams_analysis.ipynb`.
5. **Update Agents**: Register the new module in this guide and create a user story in `user_stories.md`.

## Interaction Pattern
Modules should never have circular dependencies. `Analyzer` can depend on `Processor`, but `Processor` must remain pure and independent.
