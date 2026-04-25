---
name: user-stories
description:
  Use this skill to review functional requirements, user stories, and acceptance criteria for current and future features.
---

# User Stories Skill

This document defines the functional scope of WhoSaid.APP from the user's perspective.

## Current Features (V1.0)

### US-01: Bulk Transcript Download
**As a** data researcher,
**I want to** provide a list of YouTube URLs mapped to creators,
**So that** I can automatically download and store their transcripts locally.
- **Acceptance Criteria**:
    - Supports Spanish and English.
    - Uses parallel processing.
    - Saves JSON files in creator-specific folders.

### US-02: Multi-word Pattern Extraction (N-grams)
**As a** linguistic analyst,
**I want to** identify phrases of 2 to 6 words used by a creator,
**So that** I can understand their speech patterns.
- **Acceptance Criteria**:
    - N-grams must retain exact timestamps (start/end).
    - Must handle phrases that cross transcription blocks fluently.

### US-03: Distinctive Phrase Identification (Intersection)
**As a** content analyst,
**I want to** filter phrases that appear in more than 60% of a creator's videos,
**So that** I can differentiate catchphrases from common conversational words.

## Future Features (Backlog)
- **US-04: Proxy Support**: Use a proxy list to avoid IP blocking from YouTube.
- **US-05: Sentiment Analysis Integration**: Associate N-grams with emotional tones.
- **US-06: Cross-Creator Analysis**: Compare if two creators share the same unique N-grams.
