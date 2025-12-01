"""Enhanced Search Service with Wikipedia and Google Search"""
import os
import asyncio
from typing import List, Dict, Optional
from models.research import Source
import wikipediaapi
from googlesearch import search as google_search
import requests
from bs4 import BeautifulSoup
from trafilatura import fetch_url, extract
import re


class SearchService:
    """Multi-source search service using Wikipedia and Google"""
    
    def __init__(self):
        self.mode = os.getenv("SEARCH_MODE", "demo")
        self.enable_wikipedia = os.getenv("ENABLE_WIKIPEDIA", "true").lower() == "true"
        self.enable_google = os.getenv("ENABLE_GOOGLE_SEARCH", "true").lower() == "true"
        self.enable_scraping = os.getenv("ENABLE_WEB_SCRAPING", "true").lower() == "true"
        self.max_results = int(os.getenv("MAX_SEARCH_RESULTS", "10"))
        self.timeout = int(os.getenv("SCRAPING_TIMEOUT", "10"))
        self.user_agent = os.getenv("USER_AGENT", "EliteContent-Research-Bot/1.0")
        
        # Initialize Wikipedia API
        self.wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent=self.user_agent
        )
    
    async def search(self, query: str, max_results: int = 5) -> List[Source]:
        """
        Perform multi-source search
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of Source objects from Wikipedia and Google
        """
        if self.mode == "demo":
            return self._demo_search(query, max_results)
        
        all_results = []
        
        # 1. Search Wikipedia
        if self.enable_wikipedia:
            wiki_results = await self._search_wikipedia(query)
            all_results.extend(wiki_results)
        
        # 2. Search Google
        if self.enable_google:
            google_results = await self._search_google(query, max_results)
            all_results.extend(google_results)
        
        # 3. Remove duplicates and rank
        unique_results = self._deduplicate_results(all_results)
        ranked_results = self._rank_results(unique_results, query)
        
        # 4. Extract content for top results
        if self.enable_scraping:
            top_results = ranked_results[:3]
            for result in top_results:
                if result.source_type != 'wikipedia':  # Wikipedia already has content
                    content = await self._extract_content(result.url)
                    if content:
                        result.content = content
        
        return ranked_results[:max_results]
    
    async def _search_wikipedia(self, query: str) -> List[Source]:
        """Search Wikipedia and return results"""
        results = []
        
        try:
            # Search Wikipedia
            search_results = self.wiki.search(query, results=3)
            
            for title in search_results:
                page = self.wiki.page(title)
                
                if page.exists():
                    # Get summary (first 300 chars)
                    snippet = page.summary[:300] + "..." if len(page.summary) > 300 else page.summary
                    
                    # Calculate relevance based on query match
                    relevance = self._calculate_relevance(query, page.title, snippet)
                    
                    source = Source(
                        title=page.title,
                        url=page.fullurl,
                        snippet=snippet,
                        relevance_score=relevance,
                        source_type='wikipedia',
                        content=page.text  # Full Wikipedia article
                    )
                    results.append(source)
        
        except Exception as e:
            print(f"Wikipedia search error: {str(e)}")
        
        return results
    
    async def _search_google(self, query: str, num_results: int = 5) -> List[Source]:
        """Search Google and return results"""
        results = []
        
        try:
            # Use googlesearch-python library
            search_results = list(google_search(query, num_results=num_results, lang='en'))
            
            for url in search_results:
                # Fetch page title and snippet
                title, snippet = await self._fetch_page_metadata(url)
                
                if title:
                    relevance = self._calculate_relevance(query, title, snippet)
                    
                    source = Source(
                        title=title,
                        url=url,
                        snippet=snippet,
                        relevance_score=relevance,
                        source_type='google'
                    )
                    results.append(source)
        
        except Exception as e:
            print(f"Google search error: {str(e)}")
        
        return results
    
    async def _fetch_page_metadata(self, url: str) -> tuple:
        """Fetch page title and meta description"""
        try:
            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else url
            
            # Get meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            snippet = meta_desc.get('content', '')[:300] if meta_desc else ''
            
            # If no meta description, get first paragraph
            if not snippet:
                first_p = soup.find('p')
                snippet = first_p.get_text()[:300] if first_p else ''
            
            return title_text, snippet
        
        except Exception as e:
            print(f"Error fetching metadata from {url}: {str(e)}")
            return url, ''
    
    async def _extract_content(self, url: str) -> Optional[str]:
        """Extract main content from URL using trafilatura"""
        try:
            downloaded = fetch_url(url)
            if downloaded:
                content = extract(downloaded)
                return content
        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
        
        return None
    
    def _calculate_relevance(self, query: str, title: str, snippet: str) -> float:
        """Calculate relevance score based on query match"""
        query_lower = query.lower()
        title_lower = title.lower()
        snippet_lower = snippet.lower()
        
        score = 0.0
        
        # Exact match in title (high weight)
        if query_lower in title_lower:
            score += 0.5
        
        # Word matches in title
        query_words = set(query_lower.split())
        title_words = set(title_lower.split())
        title_match_ratio = len(query_words & title_words) / len(query_words) if query_words else 0
        score += title_match_ratio * 0.3
        
        # Word matches in snippet
        snippet_words = set(snippet_lower.split())
        snippet_match_ratio = len(query_words & snippet_words) / len(query_words) if query_words else 0
        score += snippet_match_ratio * 0.2
        
        return min(1.0, score)
    
    def _deduplicate_results(self, results: List[Source]) -> List[Source]:
        """Remove duplicate URLs"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            if result.url not in seen_urls:
                seen_urls.add(result.url)
                unique_results.append(result)
        
        return unique_results
    
    def _rank_results(self, results: List[Source], query: str) -> List[Source]:
        """Rank results by relevance score"""
        # Sort by relevance score (descending)
        return sorted(results, key=lambda x: x.relevance_score, reverse=True)
    
    def _demo_search(self, query: str, max_results: int) -> List[Source]:
        """Generate demo search results"""
        demo_sources = [
            Source(
                title=f"Comprehensive Guide to {query}",
                url=f"https://example.com/guide-{query.lower().replace(' ', '-')}",
                snippet=f"This comprehensive guide covers everything you need to know about {query}, including best practices, case studies, and expert insights.",
                relevance_score=0.95,
                source_type='demo'
            ),
            Source(
                title=f"Latest Research on {query}",
                url=f"https://research.example.com/{query.lower().replace(' ', '-')}",
                snippet=f"Recent studies show significant developments in {query}. This article synthesizes the latest findings from leading researchers.",
                relevance_score=0.9,
                source_type='demo'
            ),
            Source(
                title=f"{query}: A Practical Approach",
                url=f"https://practical.example.com/{query.lower().replace(' ', '-')}",
                snippet=f"Learn practical techniques and real-world applications of {query} with this hands-on guide.",
                relevance_score=0.85,
                source_type='demo'
            ),
            Source(
                title=f"Industry Perspectives on {query}",
                url=f"https://industry.example.com/{query.lower().replace(' ', '-')}",
                snippet=f"Leading industry experts share their perspectives and predictions about the future of {query}.",
                relevance_score=0.8,
                source_type='demo'
            ),
            Source(
                title=f"Case Studies: {query} in Action",
                url=f"https://casestudies.example.com/{query.lower().replace(' ', '-')}",
                snippet=f"Explore real-world case studies demonstrating successful implementation of {query} across various industries.",
                relevance_score=0.75,
                source_type='demo'
            ),
        ]
        
        return demo_sources[:max_results]
