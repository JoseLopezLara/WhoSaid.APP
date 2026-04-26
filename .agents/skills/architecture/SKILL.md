---
name: architecture
description:
  Use this skill to understand the project's modular architecture, component responsibilities, and protocols for extending functionality.
---

# Architecture Skill

This guide explains the technical structure of WhoSaid.APP and how to extend its functionality.

## Framework-Style Architecture
The system is organized into a modular framework structure within `src/whosaid/`.

### Component Map
- **`config/`**: Centralized configurations following the "one file per library/module" rule.
    - `base.py`: System logic, secrets, and environment management.
    - `yt_dlp.py`: Library-specific configurations for `yt-dlp`.
    - `analysis.py`: Business parameters for N-grams (thresholds, sizes).
- **`common/`**: Shared business logic.
    - `storage.py`: File system hierarchy management and JSON persistence.
- **`utils/`**: Pure utility functions.
    - `helpers.py`: Supporting functions (e.g., extracting YouTube IDs).
- **`stages/`**: Primary pipeline stages.
    - **Stage 1 (Download)**: `stages/stage1_download/engine.py` (Orchestrator), `parsers.py`, `proxies.py`.
    - **Stage 2 (Analysis)**: `stages/stage2_analysis/engine.py` (Analyzer), `processor.py`.

## Extension Protocol: Adding New Features
To add a new functionality (e.g., Sentiment Analysis), follow these steps:

1. **Classify the logic**: 
    - Is it a new stage? Create `src/whosaid/stages/stage3_sentiment/`.
    - Is it a shared utility? Add to `src/whosaid/utils/` or `src/whosaid/common/`.
2. **Expose the Class**: Add the new class to `src/whosaid/__init__.py` for easy access via the facade.
3. **Integration**: Update orchestrators or create a new execution script.
4. **Update Agents**: Register the new module in this guide.

## Interaction Pattern
Modules should never have circular dependencies. `Analyzer` can depend on `Processor`, but `Processor` must remain pure and independent.
