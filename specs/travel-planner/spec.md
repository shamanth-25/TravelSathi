# Specification: RAG Travel Planner

## Goal
Improve the travel planner component to dynamically retrieve local offline travel information (e.g. festivals, local phrases, safety tips) using the RAG engine instead of pure LLM generation.

## Requirements
- Load and parse city text files from `rag/knowledge_base/`.
- Index documents with FAISS and compute sentence embeddings.
- Implement search function inside `rag/rag_engine.py`.
- Render the retrieved local knowledge in the Streamlit UI under `frontend/planner.py`.
