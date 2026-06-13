# Technical Plan: RAG Travel Planner Integration

## Architecture & Design
- Create FAISS index of files under `rag/knowledge_base/` on application startup.
- Add a similarity search function in `rag/rag_engine.py` that takes a user query and city, and returns relevant travel tips.
- Update `frontend/planner.py` to retrieve context using the RAG search function and display it in a clean section under the travel itinerary.

## Proposed Changes
- `[MODIFY]` `rag/rag_engine.py`
- `[MODIFY]` `frontend/planner.py`

## Risks & Mitigations
- Performance: Loading the embeddings models might take time. Mitigation: Cache the loaded model using Streamlit's `@st.cache_resource`.
