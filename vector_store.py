"""
Vector Store Module
Handles embeddings generation and vector database operations
"""

from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from openai import OpenAI

from config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    DB_DIR,
    COLLECTION_NAME,
    TOP_K_RESULTS,
    SIMILARITY_THRESHOLD
)


class VectorStore:
    """Manages vector embeddings and similarity search"""
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=str(DB_DIR),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "Policy documents embeddings"}
        )
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        try:
            response = self.client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Error generating embedding: {str(e)}")
    
    def add_documents(self, chunks: List[Dict[str, any]]) -> None:
        """
        Add document chunks to vector store
        
        Args:
            chunks: List of document chunks with metadata
        """
        print(f"Adding {len(chunks)} chunks to vector store...")
        
        documents = []
        embeddings = []
        metadatas = []
        ids = []
        
        for i, chunk in enumerate(chunks):
            # Generate embedding
            embedding = self.generate_embedding(chunk['text'])
            
            documents.append(chunk['text'])
            embeddings.append(embedding)
            metadatas.append(chunk['metadata'])
            ids.append(f"chunk_{chunk['chunk_id']}")
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(chunks)} chunks")
        
        # Add to ChromaDB
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"Successfully added {len(chunks)} chunks to vector store")
    
    def search(self, query: str, top_k: int = TOP_K_RESULTS) -> Dict[str, any]:
        """
        Search for relevant document chunks
        
        Args:
            query: User query
            top_k: Number of results to return
            
        Returns:
            Search results with relevance scores
        """
        # Generate query embedding
        query_embedding = self.generate_embedding(query)
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Format results
        formatted_results = []
        
        if results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                # Convert distance to similarity score (1 - normalized distance)
                distance = results['distances'][0][i]
                similarity = 1 - (distance / 2)  # Normalize to 0-1 range
                
                formatted_results.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'similarity_score': similarity
                })
        
        return {
            'query': query,
            'results': formatted_results,
            'total_results': len(formatted_results)
        }
    
    def clear_database(self) -> None:
        """Clear all documents from the vector store"""
        self.chroma_client.delete_collection(name=COLLECTION_NAME)
        self.collection = self.chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "Policy documents embeddings"}
        )
        print("Vector store cleared")
    
    def get_collection_stats(self) -> Dict[str, any]:
        """Get statistics about the collection"""
        count = self.collection.count()
        return {
            'total_chunks': count,
            'collection_name': COLLECTION_NAME
        }


class EmbeddingCache:
    """Cache for embeddings to avoid redundant API calls"""
    
    def __init__(self):
        self.cache = {}
    
    def get(self, text: str) -> Optional[List[float]]:
        """Get cached embedding"""
        return self.cache.get(text)
    
    def set(self, text: str, embedding: List[float]) -> None:
        """Cache embedding"""
        self.cache[text] = embedding
    
    def clear(self) -> None:
        """Clear cache"""
        self.cache = {}
