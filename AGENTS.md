# WhoSaid.APP - AI Agents Orchestrator

This document serves as the master guide for AI agents (Gemini CLI, Jules) interacting with this repository. You MUST consult this agent at the start of every session to align with project standards.

## Core Engineering Principles
- **Language**: All code (variables, classes, comments) and documentation MUST be in English.
- **Single Responsibility (SRP)**: Every function or class must perform one, and only one, action.
- **Modular Architecture**: Favor composition over inheritance. Always separate logic (src/) from orchestration (Notebooks).
- **Type Safety**: Use Python type hints (`from typing import ...`) for all new functions.

## Mandatory Repetitive Actions (Workflow)
1. **Research Phase**: Before implementing any library-specific logic, consult `agents/official_documentation_sources.md`.
2. **Sync Phase**: If a Business Rule or Architecture changes during your task, you MUST update the corresponding agent in `/agents` before finishing.
3. **Validation**: Every change must be verified against existing user stories in `agents/user_stories.md`.

## Available Specialized Agents
| Agent | Purpose | When to consult? |
| :--- | :--- | :--- |
| [Architecture Guide](agents/architecture_guide.md) | Technical patterns and module interaction. | When adding new features or refactoring. |
| [Official Documentation](agents/official_documentation_sources.md) | Approved libraries and documentation URLs. | Before using external tools or APIs. |
| [Business Rules](agents/youtube_ngram_extraction_logic.md) | Logic for N-grams, Union, and Intersection. | When changing how data is processed. |
| [User Stories](agents/user_stories.md) | Functional requirements and test cases. | To validate the "What" and "Why" of a task. |

## Self-Documentation Protocol
If you modify the system, you must update the agents following this hierarchy:
1. **Architecture Change?** Update `architecture_guide.md`.
2. **Logic/Algorithm Change?** Update `youtube_ngram_extraction_logic.md`.
3. **New Feature?** Add a new entry to `user_stories.md`.
