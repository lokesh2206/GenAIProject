"""
Vector Store Module - Manage Chroma vector database
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from config.settings import settings
import uuid

class VectorStore:
    """Manage Chroma vector database for semantic search"""
    
    def __init__(self, persist_directory: str = None):
        """
        Initialize vector store
        
        Args:
            persist_directory: Directory to persist the vector database
        """
        self.persist_directory = persist_directory or settings.CHROMA_PERSIST_DIRECTORY
        self.client = None
        self.collection = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Chroma client"""
        try:
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            print(f"Initialized Chroma client at: {self.persist_directory}")
        except Exception as e:
            raise Exception(f"Error initializing Chroma client: {str(e)}")
    
    def create_collection(self, collection_name: str = "data_schema"):
        """
        Create or get a collection
        
        Args:
            collection_name: Name of the collection
        """
        try:
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "Data schema and metadata embeddings"}
            )
            print(f"Collection '{collection_name}' ready")
        except Exception as e:
            raise Exception(f"Error creating collection: {str(e)}")
    
    def add_documents(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ):
        """
        Add documents to the collection
        
        Args:
            documents: List of text documents
            embeddings: List of embedding vectors
            metadatas: Optional metadata for each document
            ids: Optional IDs for each document
        """
        if not self.collection:
            raise ValueError("Collection not initialized. Call create_collection first.")
        
        if not documents or not embeddings:
            raise ValueError("Documents and embeddings cannot be empty")
        
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents must match number of embeddings")
        
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in range(len(documents))]
        
        # Add default metadata if not provided
        if metadatas is None:
            metadatas = [{"source": "csv_schema"} for _ in range(len(documents))]
        
        try:
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Added {len(documents)} documents to collection")
        except Exception as e:
            raise Exception(f"Error adding documents: {str(e)}")
    
    def query(
        self,
        query_embeddings: List[List[float]],
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query the collection
        
        Args:
            query_embeddings: Query embedding vectors
            n_results: Number of results to return
            where: Optional filter conditions
            
        Returns:
            Query results
        """
        if not self.collection:
            raise ValueError("Collection not initialized. Call create_collection first.")
        
        try:
            results = self.collection.query(
                query_embeddings=query_embeddings,
                n_results=n_results,
                where=where
            )
            return results
        except Exception as e:
            raise Exception(f"Error querying collection: {str(e)}")
    
    def get_collection_count(self) -> int:
        """Get the number of documents in the collection"""
        if not self.collection:
            return 0
        return self.collection.count()
    
    def delete_collection(self, collection_name: str):
        """Delete a collection"""
        try:
            self.client.delete_collection(name=collection_name)
            print(f"Deleted collection: {collection_name}")
        except Exception as e:
            print(f"Error deleting collection: {str(e)}")
    
    def reset(self):
        """Reset the vector store (delete all collections)"""
        try:
            self.client.reset()
            print("Vector store reset successfully")
        except Exception as e:
            print(f"Error resetting vector store: {str(e)}")
