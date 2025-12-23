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
    SIMILARITY_THRESHOLD,
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    LOCAL_EMBEDDING_MODEL,
    USE_LOCAL_EMBEDDINGS
)


class VectorStore:
    """Manages vector embeddings and similarity search"""
    
    def __init__(self):
        # Initialize Client based on configuration
        if DEEPSEEK_API_KEY:
            self.client = OpenAI(
                api_key=DEEPSEEK_API_KEY,
                base_url=DEEPSEEK_BASE_URL
            )
        else:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            
        # Initialize Local Embedding Model if configured
        self.embedding_model = None
        if USE_LOCAL_EMBEDDINGS:
            from sentence_transformers import SentenceTransformer
            self.embedding_model = SentenceTransformer(LOCAL_EMBEDDING_MODEL)
        
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
        Generate embedding for text
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        try:
            if USE_LOCAL_EMBEDDINGS and self.embedding_model:
                # Use local sentence-transformers
                embedding = self.embedding_model.encode(text)
                return embedding.tolist()
            else:
                # Use OpenAI API
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
        
        texts = [chunk['text'] for chunk in chunks]
        
        # Generate embeddings
        if USE_LOCAL_EMBEDDINGS and self.embedding_model:
            print("Generating embeddings in batch (local model)...")
            embeddings_array = self.embedding_model.encode(texts, show_progress_bar=True)
            embeddings = embeddings_array.tolist()
        else:
            print("Generating embeddings using API...")
            for i, text in enumerate(texts):
                embedding = self.generate_embedding(text)
                embeddings.append(embedding)
                if (i + 1) % 10 == 0:
                    print(f"Processed {i + 1}/{len(chunks)} chunks")
        
        # Prepare other data
        for i, chunk in enumerate(chunks):
            documents.append(chunk['text'])
            metadatas.append(chunk['metadata'])
            # Create a unique ID combining filename and chunk index
            unique_id = f"{chunk['metadata']['filename']}_{chunk['chunk_id']}"
            # Remove spaces and special chars from ID to be safe
            unique_id = "".join(c for c in unique_id if c.isalnum() or c in "_-")
            ids.append(unique_id)
        
        # Add to ChromaDB in batches to avoid payload size issues
        batch_size = 500
        total_batches = (len(documents) + batch_size - 1) // batch_size
        
        print(f"\nInserting into ChromaDB in {total_batches} batches...")
        
        for i in range(0, len(documents), batch_size):
            end = min(i + batch_size, len(documents))
            self.collection.add(
                documents=documents[i:end],
                embeddings=embeddings[i:end],
                metadatas=metadatas[i:end],
                ids=ids[i:end]
            )
            print(f"Inserted batch {i//batch_size + 1}/{total_batches}")
        
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
