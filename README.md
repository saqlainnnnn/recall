# Recall

A multimodal, lifecycle-based external memory layer for LLMs.

Recall is designed to extract, store, update, delete, and retrieve
useful memories from text, images, documents, and audio.

## Architecture

- SQLite as the canonical source of truth
- FAISS for dense vector retrieval
- BM25 for sparse keyword retrieval
- Configurable LLM, embedding, vision, and transcription providers
- A shared memory lifecycle: ADD, UPDATE, DELETE, NONE

## Development

Requires Python 3.12.

Create and activate a virtual environment, then install development
dependencies:

    python3.12 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -e ".[dev]"

Run tests:

    pytest

Run lint checks:

    ruff check .
    ruff format --check .

## Project status

Initial project scaffold. Core functionality will be implemented
incrementally with tests and documented acceptance criteria.

## Scope exclusions

- Graph databases and graph-based memory
- Training or fine-tuning neural memory models
- Distributed infrastructure and hosted management dashboards
