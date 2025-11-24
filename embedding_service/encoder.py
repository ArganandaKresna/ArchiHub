# embedding_service/encoder.py
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingGenerator:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.embedding_size = 384  # Size for all-MiniLM-L6-v2
    
    def encode(self, text: str) -> List[float]:
        """Generate embedding for text"""
        if not text or text.strip() == "":
            # Return zero vector for empty text
            return [0.0] * self.embedding_size
        
        embedding = self.model.encode(text)
        return embedding.tolist()
    
    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        if not texts:
            return []
        
        embeddings = self.model.encode(texts)
        return embeddings.tolist()