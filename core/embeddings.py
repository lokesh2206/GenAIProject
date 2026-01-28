"""
Embeddings Module - Generate embeddings using SentenceTransformers
"""
from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np
from config.settings import settings

class EmbeddingGenerator:
    """Generate embeddings for text using SentenceTransformers"""
    
    def __init__(self, model_name: str = None):
        """
        Initialize embedding generator
        
        Args:
            model_name: Name of the SentenceTransformer model
        """
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the SentenceTransformer model"""
        try:
            self.model = SentenceTransformer(self.model_name)
            print(f"Loaded embedding model: {self.model_name}")
        except Exception as e:
            raise Exception(f"Error loading embedding model: {str(e)}")
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector as numpy array
        """
        if not text or not isinstance(text, str):
            raise ValueError("Input must be a non-empty string")
        
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def generate_embeddings(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of input texts
            batch_size: Batch size for processing
            
        Returns:
            Array of embedding vectors
        """
        if not texts:
            raise ValueError("Input list cannot be empty")
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=len(texts) > 10
        )
        return embeddings
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embedding vectors"""
        return self.model.get_sentence_embedding_dimension()
