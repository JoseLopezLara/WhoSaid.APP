# WhoSaid.APP - AI Agents Orchestrator

This document serves as the master guide for AI agents (Gemini CLI, Jules) interacting with this repository. You MUST consult this agent at the start of every session to align with project standards.

## Core Engineering Principles
- **Language**: ALL code (variables, functions, classes), comments, logs, and documentation MUST be in English. No exceptions.
- **Single Responsibility (SRP)**: Every function or class must perform one, and only one, action.
- **Modular Architecture**: Framework-style design. Separate core logic from stage-specific implementations.
- **Evasion & Integrity**: When fetching external data (YouTube), use modular configurations and human-like behavior (random sleeps, client spoofing) to ensure service continuity.
- **Type Safety**: Use Python type hints (`from typing import ...`) for all new functions.

## Mandatory Repetitive Actions (Workflow)
1. **Research Phase**: Before implementing any library-specific logic, consult the `documentation` skill.
2. **Sync Phase**: If a Business Rule or Architecture changes during your task, you MUST update the corresponding skill in `.agents/skills/` before finishing.
3. **Validation**: Every change must be verified against existing user stories in the `user-stories` skill.

## Available Specialized Skills (Native Gemini CLI Skills)
| Skill | Purpose | Activation Command |
| :--- | :--- | :--- |
| **architecture** | Technical patterns and module interaction. | `/activate_skill architecture` |
| **documentation** | Approved libraries and documentation URLs. | `/activate_skill documentation` |
| **business-logic** | Logic for N-grams, Union, and Intersection. | `/activate_skill business-logic` |
| **user-stories** | Functional requirements and test cases. | `/activate_skill user-stories` |

## Self-Documentation Protocol
If you modify the system, you must update the skills following this hierarchy:
1. **Architecture Change?** Update `.agents/skills/architecture/SKILL.md`.
2. **Logic/Algorithm Change?** Update `.agents/skills/business-logic/SKILL.md`.
3. **New Feature?** Add a new entry to `.agents/skills/user-stories/SKILL.md`.
