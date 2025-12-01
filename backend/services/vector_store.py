"""Vector Store Service using ChromaDB for RAG"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import os
from sentence_transformers import SentenceTransformer


class VectorStore:
    """ChromaDB vector store for document embeddings and semantic search"""
    
    def __init__(self):
        # Get configuration from environment
        persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
        embedding_model = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        use_local = os.getenv("USE_LOCAL_EMBEDDINGS", "true").lower() == "true"
        
        # Initialize ChromaDB client with new API
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # Initialize embedding model
        if use_local:
            print(f"🔧 Loading local embedding model: {embedding_model}")
            self.embedding_model = SentenceTransformer(embedding_model)
        else:
            self.embedding_model = None  # Will use OpenAI embeddings
        
        # Create or get collections
        self.research_collection = self.client.get_or_create_collection(
            name="research_documents",
            metadata={"description": "Research documents and sources"}
        )
        
        print(f"✅ VectorStore initialized with {self.research_collection.count()} documents")
    
    def add_documents(
        self, 
        documents: List[str], 
        metadatas: List[Dict], 
        ids: List[str]
    ):
        """
        Add documents to vector store
        
        Args:
            documents: List of document texts
            metadatas: List of metadata dicts
            ids: List of unique IDs
        """
        try:
            # Generate embeddings if using local model
            if self.embedding_model:
                embeddings = self.embedding_model.encode(documents).tolist()
                self.research_collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids,
                    embeddings=embeddings
                )
            else:
                # ChromaDB will use default embedding function
                self.research_collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
            
            print(f"✅ Added {len(documents)} documents to vector store")
        except Exception as e:
            print(f"❌ Error adding documents: {str(e)}")
    
    def search(self, query: str, n_results: int = 5) -> Dict:
        """
        Semantic search in vector store
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            Dict with documents, metadatas, distances
        """
        try:
            # Generate query embedding if using local model
            if self.embedding_model:
                query_embedding = self.embedding_model.encode([query]).tolist()[0]
                results = self.research_collection.query(
                    query_embeddings=[query_embedding],
                    n_results=n_results
                )
            else:
                results = self.research_collection.query(
                    query_texts=[query],
                    n_results=n_results
                )
            
            return results
        except Exception as e:
            print(f"❌ Error searching: {str(e)}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    
    def get_relevant_context(self, query: str, max_tokens: int = 2000) -> str:
        """
        Get relevant context for RAG
        
        Args:
            query: Search query
            max_tokens: Maximum tokens for context (approximate)
            
        Returns:
            Formatted context string
        """
        results = self.search(query, n_results=5)
        
        if not results['documents'] or not results['documents'][0]:
            return ""
        
        # Combine top results into context
        context_parts = []
        total_chars = 0
        max_chars = max_tokens * 4  # Rough approximation
        
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            if total_chars >= max_chars:
                break
            
            source = metadata.get('title', 'Unknown')
            url = metadata.get('url', '')
            source_type = metadata.get('source_type', 'web')
            
            context_part = f"**Source [{source_type.upper()}]:** {source}\n"
            if url:
                context_part += f"**URL:** {url}\n"
            context_part += f"**Content:**\n{doc}\n"
            
            context_parts.append(context_part)
            total_chars += len(context_part)
        
        return "\n---\n".join(context_parts)
    
    def clear_collection(self):
        """Clear all documents from collection"""
        try:
            self.client.delete_collection("research_documents")
            self.research_collection = self.client.get_or_create_collection(
                name="research_documents",
                metadata={"description": "Research documents and sources"}
            )
            print("✅ Collection cleared")
        except Exception as e:
            print(f"❌ Error clearing collection: {str(e)}")
    
    def get_stats(self) -> Dict:
        """Get vector store statistics"""
        return {
            "total_documents": self.research_collection.count(),
            "collection_name": self.research_collection.name,
            "embedding_model": os.getenv("EMBEDDING_MODEL", "default")
        }
