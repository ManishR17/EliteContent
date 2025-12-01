"""Universal RAG service for all content types"""
import os
import hashlib
from typing import List, Dict, Optional
from datetime import datetime
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings


class UniversalRAG:
    """RAG service that makes all content types context-aware"""
    
    def __init__(self):
        # Initialize ChromaDB client with new API
        persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # Initialize embedding model
        embedding_model = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Create collections for each content type
        self.collections = {
            'resumes': self._get_or_create_collection('resumes', 
                "Resume content and job matches"),
            'documents': self._get_or_create_collection('documents',
                "Generated documents and templates"),
            'emails': self._get_or_create_collection('emails',
                "Email content and templates"),
            'social': self._get_or_create_collection('social_media',
                "Social media posts and hashtags"),
            'creative': self._get_or_create_collection('creative_content',
                "Creative writing and blog posts"),
            'job_descriptions': self._get_or_create_collection('job_descriptions',
                "Job descriptions and keywords"),
            'hashtags': self._get_or_create_collection('hashtags',
                "Hashtag patterns and trends")
        }
        
        print(f"✅ Universal RAG initialized with {len(self.collections)} collections")
    
    def _get_or_create_collection(self, name: str, description: str):
        """Get or create a collection"""
        try:
            return self.client.get_collection(name)
        except:
            return self.client.create_collection(
                name=name,
                metadata={"description": description}
            )
    
    # ==================== STORAGE ====================
    
    def store_content(
        self, 
        content_type: str, 
        content: str, 
        metadata: Dict
    ) -> str:
        """
        Store generated content in appropriate collection
        
        Args:
            content_type: Type of content (resumes, documents, etc.)
            content: The actual content text
            metadata: Additional metadata (user_id, timestamp, etc.)
            
        Returns:
            Document ID
        """
        if content_type not in self.collections:
            raise ValueError(f"Unknown content type: {content_type}")
        
        collection = self.collections[content_type]
        
        # Generate unique ID
        doc_id = f"{content_type}_{hashlib.md5(content.encode()).hexdigest()}"
        
        # Add timestamp
        metadata['stored_at'] = datetime.now().isoformat()
        
        # Generate embedding
        embedding = self.embedding_model.encode([content]).tolist()[0]
        
        # Store in collection
        collection.add(
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[doc_id]
        )
        
        print(f"✅ Stored {content_type} content: {doc_id[:20]}...")
        return doc_id
    
    # ==================== RETRIEVAL ====================
    
    def get_similar_content(
        self, 
        content_type: str, 
        query: str, 
        n_results: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Get similar past content for context
        
        Args:
            content_type: Type of content to search
            query: Search query
            n_results: Number of results
            filter_metadata: Optional metadata filters
            
        Returns:
            List of similar content with metadata
        """
        if content_type not in self.collections:
            return []
        
        collection = self.collections[content_type]
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()[0]
        
        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_metadata
        )
        
        # Format results
        similar_content = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                similar_content.append({
                    'content': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else 0,
                    'similarity': 1 - results['distances'][0][i] if results['distances'] else 1
                })
        
        return similar_content
    
    # ==================== RESUME-SPECIFIC ====================
    
    def extract_job_keywords(self, job_description: str) -> List[str]:
        """
        Extract keywords from job description using semantic analysis
        
        Args:
            job_description: Job description text
            
        Returns:
            List of important keywords
        """
        # Store job description for future matching
        self.store_content('job_descriptions', job_description, {
            'type': 'job_description',
            'extracted_at': datetime.now().isoformat()
        })
        
        # Use AI to extract keywords (simplified version)
        # In production, use NER or keyword extraction model
        words = job_description.lower().split()
        
        # Common important keywords in job descriptions
        important_categories = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'machine learning', 'ai', 'data science', 'analytics',
            'leadership', 'management', 'agile', 'scrum',
            'bachelor', 'master', 'phd', 'degree'
        ]
        
        keywords = []
        for category in important_categories:
            if category in job_description.lower():
                keywords.append(category)
        
        return keywords[:10]  # Top 10 keywords
    
    def match_resume_to_job(self, resume_text: str, job_description: str) -> Dict:
        """
        Calculate semantic similarity between resume and job
        
        Args:
            resume_text: Resume content
            job_description: Job description
            
        Returns:
            Match analysis with score and details
        """
        # Generate embeddings
        resume_embedding = self.embedding_model.encode([resume_text])[0]
        job_embedding = self.embedding_model.encode([job_description])[0]
        
        # Calculate cosine similarity
        from numpy import dot
        from numpy.linalg import norm
        
        similarity = dot(resume_embedding, job_embedding) / (norm(resume_embedding) * norm(job_embedding))
        match_score = float(similarity) * 100  # Convert to percentage
        
        # Extract keywords
        job_keywords = self.extract_job_keywords(job_description)
        
        # Check keyword presence
        keywords_present = [kw for kw in job_keywords if kw.lower() in resume_text.lower()]
        keywords_missing = [kw for kw in job_keywords if kw.lower() not in resume_text.lower()]
        
        return {
            'match_score': round(match_score, 2),
            'similarity': round(float(similarity), 4),
            'keywords_present': keywords_present,
            'keywords_missing': keywords_missing,
            'keyword_coverage': round(len(keywords_present) / len(job_keywords) * 100, 2) if job_keywords else 0,
            'recommendation': self._get_match_recommendation(match_score)
        }
    
    def _get_match_recommendation(self, score: float) -> str:
        """Get recommendation based on match score"""
        if score >= 80:
            return "Excellent match! Resume aligns very well with job requirements."
        elif score >= 60:
            return "Good match. Consider adding more relevant keywords."
        elif score >= 40:
            return "Moderate match. Significant improvements needed."
        else:
            return "Low match. Consider tailoring resume more closely to job description."
    
    # ==================== SOCIAL MEDIA-SPECIFIC ====================
    
    def recommend_hashtags(
        self, 
        content: str, 
        platform: str,
        n_hashtags: int = 5
    ) -> List[Dict]:
        """
        Recommend hashtags using semantic search
        
        Args:
            content: Post content
            platform: Social media platform
            n_hashtags: Number of hashtags to recommend
            
        Returns:
            List of recommended hashtags with scores
        """
        # Get similar posts
        similar_posts = self.get_similar_content('social', content, n_results=10)
        
        # Extract hashtags from similar posts
        hashtag_counts = {}
        for post in similar_posts:
            metadata = post.get('metadata', {})
            if 'hashtags' in metadata:
                for tag in metadata['hashtags']:
                    hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1
        
        # Sort by frequency
        recommended = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Format results
        hashtags = []
        for tag, count in recommended[:n_hashtags]:
            hashtags.append({
                'hashtag': tag,
                'frequency': count,
                'relevance': count / len(similar_posts) if similar_posts else 0
            })
        
        # If no hashtags found, generate generic ones
        if not hashtags:
            # Extract keywords from content
            words = content.lower().split()
            hashtags = [
                {'hashtag': f'#{word}', 'frequency': 1, 'relevance': 0.5}
                for word in words[:n_hashtags]
                if len(word) > 4
            ]
        
        return hashtags
    
    def get_trending_topics(self, platform: str, days: int = 7) -> List[Dict]:
        """
        Get trending topics from past posts
        
        Args:
            platform: Social media platform
            days: Number of days to look back
            
        Returns:
            List of trending topics
        """
        # Get recent posts
        recent_posts = self.get_similar_content(
            'social',
            '',  # Empty query gets recent items
            n_results=50
        )
        
        # Extract topics (simplified - in production use topic modeling)
        topics = {}
        for post in recent_posts:
            metadata = post.get('metadata', {})
            if 'topic' in metadata:
                topic = metadata['topic']
                topics[topic] = topics.get(topic, 0) + 1
        
        # Sort by frequency
        trending = sorted(topics.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {'topic': topic, 'count': count, 'trending_score': count / len(recent_posts)}
            for topic, count in trending[:10]
        ]
    
    # ==================== DOCUMENT-SPECIFIC ====================
    
    def get_template_suggestions(
        self, 
        doc_type: str, 
        topic: str,
        n_templates: int = 3
    ) -> List[Dict]:
        """
        Get relevant templates from past documents
        
        Args:
            doc_type: Type of document
            topic: Document topic
            n_templates: Number of templates
            
        Returns:
            List of template suggestions
        """
        # Search for similar documents
        similar_docs = self.get_similar_content(
            'documents',
            topic,
            n_results=n_templates,
            filter_metadata={'document_type': doc_type} if doc_type else None
        )
        
        # Format as templates
        templates = []
        for doc in similar_docs:
            templates.append({
                'content': doc['content'],
                'metadata': doc['metadata'],
                'similarity': doc['similarity'],
                'template_type': doc['metadata'].get('document_type', 'unknown')
            })
        
        return templates
    
    # ==================== ANALYTICS ====================
    
    def get_collection_stats(self, content_type: str) -> Dict:
        """Get statistics for a collection"""
        if content_type not in self.collections:
            return {}
        
        collection = self.collections[content_type]
        count = collection.count()
        
        return {
            'content_type': content_type,
            'total_documents': count,
            'collection_name': collection.name,
            'description': collection.metadata.get('description', '')
        }
    
    def get_all_stats(self) -> Dict:
        """Get statistics for all collections"""
        stats = {}
        total_docs = 0
        
        for content_type in self.collections:
            collection_stats = self.get_collection_stats(content_type)
            stats[content_type] = collection_stats
            total_docs += collection_stats.get('total_documents', 0)
        
        return {
            'collections': stats,
            'total_documents': total_docs,
            'embedding_model': os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        }
