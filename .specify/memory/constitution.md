# Spec-Kit Constitution

This document defines the non-negotiable principles, development standards, and architecture for the TravelSathi codebase.

## Core Directives

1. **Language & Frameworks**:
   - Backend logic is in Python 3.11+.
   - Frontend is a Streamlit application.
   - Use modular structure (e.g. `backend/ai_engine.py`, `rag/rag_engine.py`, `frontend/`).

2. **Quality & Formatting**:
   - Lint with **Ruff** before committing.
   - Use strict type annotations and check types using **Mypy**.
   - No dead/unused code (clean files with Vulture if needed).

3. **Security Standards**:
   - Never commit API keys, tokens, or credentials to git.
   - Use environment variables (via `.env` / `.env.example`).
   - Run dependency audits (`pip-audit`) and secret scanning (`gitleaks`) on CI.

4. **Testing & Coverage**:
   - Write unit tests for all new utilities/backends under `backend/test_*.py`.
   - Maintain 80%+ test coverage.

5. **Spec-Driven Development (SDD)**:
   - For any new feature, create a spec under `specs/` following `spec-template.md`.
   - Formulate a technical design in `plan.md` using `plan-template.md`.
   - Breakdown work into `tasks.md` using `tasks-template.md` before coding.
