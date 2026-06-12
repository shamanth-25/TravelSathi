import os
import re
import logging
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rag_engine")

# Try to import FAISS and SentenceTransformers for high-quality RAG
try:
    import faiss
    from sentence_transformers import SentenceTransformer
    HAS_LOCAL_RAG = True
    logger.info("Successfully imported faiss and sentence-transformers. Using advanced local RAG.")
except ImportError as e:
    HAS_LOCAL_RAG = False
    logger.warning(
        f"Could not import faiss or sentence-transformers ({str(e)}). "
        "Falling back to simple TF-IDF and word-matching retrieval."
    )

# Standard Fallback TF-IDF engine
class SimpleTFIDFEngine:
    """A lightweight in-memory vector space model fallback using TF-IDF and numpy."""
    def __init__(self, documents):
        self.documents = [doc for doc in documents if doc.strip()]
        if not self.documents:
            self.vocab = {}
            self.tfidf_matrix = np.array([])
            return
        
        # Tokenize and build vocabulary
        self.vocab = {}
        tokenized_docs = []
        for doc in self.documents:
            tokens = self._tokenize(doc)
            tokenized_docs.append(tokens)
            for token in tokens:
                if token not in self.vocab:
                    self.vocab[token] = len(self.vocab)
        
        vocab_size = len(self.vocab)
        num_docs = len(self.documents)
        
        if vocab_size == 0:
            self.tfidf_matrix = np.zeros((num_docs, 1))
            return

        # Compute Term Frequency (TF)
        tf = np.zeros((num_docs, vocab_size))
        for i, tokens in enumerate(tokenized_docs):
            for token in tokens:
                tf[i, self.vocab[token]] += 1
            # Normalize TF
            doc_len = len(tokens)
            if doc_len > 0:
                tf[i] /= doc_len
        
        # Compute Inverse Document Frequency (IDF)
        df = np.sum(tf > 0, axis=0)
        idf = np.log((1 + num_docs) / (1 + df)) + 1
        
        # Compute TF-IDF
        self.tfidf_matrix = tf * idf
        self.idf = idf

    def _tokenize(self, text):
        # Clean and tokenize text
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def search(self, query, top_k=2):
        if not self.documents or not self.vocab:
            return []
        
        # Tokenize query
        query_tokens = self._tokenize(query)
        query_tf = np.zeros(len(self.vocab))
        for token in query_tokens:
            if token in self.vocab:
                query_tf[self.vocab[token]] += 1
        
        query_len = len(query_tokens)
        if query_len > 0:
            query_tf /= query_len
            
        query_tfidf = query_tf * self.idf
        
        # Compute cosine similarities
        dot_products = np.dot(self.tfidf_matrix, query_tfidf)
        doc_norms = np.linalg.norm(self.tfidf_matrix, axis=1)
        query_norm = np.linalg.norm(query_tfidf)
        
        if query_norm == 0:
            return self.documents[:top_k]
        
        norms = doc_norms * query_norm
        # Prevent division by zero
        norms[norms == 0] = 1e-9
        similarities = dot_products / norms
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [self.documents[idx] for idx in top_indices]


class RAGEngine:
    def __init__(self, kb_dir=None):
        if kb_dir is None:
            # Locate relative to this file
            kb_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_base")
        
        self.kb_dir = kb_dir
        self.supported_cities = ["hyderabad", "varanasi", "jaipur"]
        
        # Documents grouped by city
        self.city_documents = {city: [] for city in self.supported_cities}
        
        # Load and chunk documents
        self._load_knowledge_base()
        
        # Initialize search indices
        self.embedding_model = None
        self.faiss_indices = {}
        self.fallback_engines = {}
        
        if HAS_LOCAL_RAG:
            try:
                logger.info("Initializing SentenceTransformer model (all-MiniLM-L6-v2)...")
                # Using a highly-optimized, fast and small sentence transformer
                self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
                self._build_faiss_indices()
            except Exception as e:
                logger.error(f"Error loading embedding model or building FAISS: {str(e)}. Falling back.")
                self._build_fallback_engines()
        else:
            self._build_fallback_engines()

    def _load_knowledge_base(self):
        """Loads and chunks city documents from the text files."""
        for city in self.supported_cities:
            file_path = os.path.join(self.kb_dir, f"{city}.txt")
            if not os.path.exists(file_path):
                logger.warning(f"Knowledge base file not found for {city}: {file_path}")
                continue
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Chunking: split by double newlines to keep paragraph semantic structure intact
                paragraphs = content.split("\n\n")
                chunks = []
                for p in paragraphs:
                    p_clean = p.strip()
                    if p_clean:
                        # Append the city context if not already present, to enrich embedding quality
                        if not p_clean.lower().startswith(f"city:"):
                            p_clean = f"City: {city.capitalize()}\n{p_clean}"
                        chunks.append(p_clean)
                
                self.city_documents[city] = chunks
                logger.info(f"Loaded {len(chunks)} chunks for {city}.")
            except Exception as e:
                logger.error(f"Failed to load/chunk {file_path}: {str(e)}")

    def _build_faiss_indices(self):
        """Builds a FAISS index per city for isolated, high-performance retrieval."""
        for city in self.supported_cities:
            chunks = self.city_documents.get(city, [])
            if not chunks:
                logger.warning(f"No chunks found to index for city: {city}")
                continue
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(chunks, show_progress_bar=False)
            embeddings = np.array(embeddings).astype("float32")
            
            # Create FAISS flat index
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings)
            
            self.faiss_indices[city] = index
            logger.info(f"Built FAISS index for {city} with dimension {dimension}.")

    def _build_fallback_engines(self):
        """Builds TF-IDF engines for cities when FAISS/SentenceTransformers are unavailable."""
        logger.info("Building TF-IDF engines for fallback search.")
        for city in self.supported_cities:
            chunks = self.city_documents.get(city, [])
            self.fallback_engines[city] = SimpleTFIDFEngine(chunks)

    def retrieve(self, query, city, top_k=2):
        """Retrieves top_k relevant documents for the given query and city."""
        city_lower = city.lower()
        if city_lower not in self.supported_cities:
            logger.warning(f"City '{city}' is not supported by RAG. Supported: {self.supported_cities}")
            return []
            
        chunks = self.city_documents.get(city_lower, [])
        if not chunks:
            logger.warning(f"No chunks available for city: {city_lower}")
            return []

        # If we have FAISS index, use it
        if HAS_LOCAL_RAG and city_lower in self.faiss_indices and self.embedding_model:
            try:
                # Generate query embedding
                query_emb = self.embedding_model.encode([query], show_progress_bar=False)
                query_emb = np.array(query_emb).astype("float32")
                
                # Search FAISS index
                index = self.faiss_indices[city_lower]
                # Adjust top_k to not exceed document count
                actual_k = min(top_k, len(chunks))
                if actual_k <= 0:
                    return []
                    
                distances, indices = index.search(query_emb, actual_k)
                
                retrieved = []
                for idx in indices[0]:
                    if 0 <= idx < len(chunks):
                        retrieved.append(chunks[idx])
                return retrieved
            except Exception as e:
                logger.error(f"Error querying FAISS for {city_lower}: {str(e)}. Using fallback TF-IDF.")
                # Fallback on failure
                if city_lower not in self.fallback_engines:
                    self.fallback_engines[city_lower] = SimpleTFIDFEngine(chunks)
                return self.fallback_engines[city_lower].search(query, top_k)
        else:
            # Use fallback TF-IDF
            if city_lower not in self.fallback_engines:
                self.fallback_engines[city_lower] = SimpleTFIDFEngine(chunks)
            return self.fallback_engines[city_lower].search(query, top_k)


# Singleton instance for global reuse
_rag_engine_instance = None

def get_rag_engine():
    global _rag_engine_instance
    if _rag_engine_instance is None:
        _rag_engine_instance = RAGEngine()
    return _rag_engine_instance
