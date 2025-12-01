"""MCP integrations for GitHub, arXiv, and PubMed"""
import httpx
import os
from typing import List, Dict, Optional
import xmltodict
from models.research import Source


class GitHubMCP:
    """GitHub API integration for code and repository search"""
    
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.enabled = os.getenv("ENABLE_GITHUB", "true").lower() == "true"
    
    async def search_repositories(self, query: str, max_results: int = 5) -> List[Source]:
        """Search GitHub repositories"""
        if not self.enabled:
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                headers = {}
                if self.token and self.token != "your-github-token-here":
                    headers["Authorization"] = f"token {self.token}"
                
                response = await client.get(
                    f"{self.base_url}/search/repositories",
                    params={"q": query, "per_page": max_results, "sort": "stars"},
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    items = response.json().get("items", [])
                    sources = []
                    
                    for item in items:
                        # Get README content
                        readme = await self._get_readme(item["full_name"], headers)
                        
                        source = Source(
                            title=f"{item['full_name']} - {item.get('description', 'No description')}",
                            url=item["html_url"],
                            snippet=item.get("description", "")[:300],
                            relevance_score=min(item.get("stargazers_count", 0) / 10000, 1.0),
                            source_type="github",
                            content=readme if readme else item.get("description", "")
                        )
                        sources.append(source)
                    
                    return sources
        except Exception as e:
            print(f"GitHub search error: {str(e)}")
        
        return []
    
    async def _get_readme(self, repo_full_name: str, headers: dict) -> Optional[str]:
        """Get repository README"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/repos/{repo_full_name}/readme",
                    headers={**headers, "Accept": "application/vnd.github.v3.raw"},
                    timeout=5.0
                )
                return response.text if response.status_code == 200 else None
        except:
            return None


class ArXivMCP:
    """arXiv API integration for academic papers"""
    
    def __init__(self):
        self.base_url = "http://export.arxiv.org/api/query"
        self.enabled = os.getenv("ENABLE_ARXIV", "true").lower() == "true"
    
    async def search_papers(self, query: str, max_results: int = 5) -> List[Source]:
        """Search arXiv papers"""
        if not self.enabled:
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.base_url,
                    params={
                        "search_query": f"all:{query}",
                        "max_results": max_results,
                        "sortBy": "relevance"
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return self._parse_arxiv_response(response.text)
        except Exception as e:
            print(f"arXiv search error: {str(e)}")
        
        return []
    
    def _parse_arxiv_response(self, xml_text: str) -> List[Source]:
        """Parse arXiv XML response"""
        try:
            data = xmltodict.parse(xml_text)
            feed = data.get("feed", {})
            entries = feed.get("entry", [])
            
            # Handle single entry
            if isinstance(entries, dict):
                entries = [entries]
            
            sources = []
            for i, entry in enumerate(entries):
                title = entry.get("title", "").replace("\n", " ").strip()
                summary = entry.get("summary", "").replace("\n", " ").strip()
                link = entry.get("id", "")
                
                # Get authors
                authors = entry.get("author", [])
                if isinstance(authors, dict):
                    authors = [authors]
                author_names = [a.get("name", "") for a in authors]
                author_str = ", ".join(author_names[:3])
                if len(author_names) > 3:
                    author_str += " et al."
                
                source = Source(
                    title=f"{title} ({author_str})",
                    url=link,
                    snippet=summary[:300],
                    relevance_score=1.0 - (i * 0.1),  # Decrease by position
                    source_type="arxiv",
                    content=f"Title: {title}\n\nAuthors: {author_str}\n\nAbstract: {summary}"
                )
                sources.append(source)
            
            return sources
        except Exception as e:
            print(f"arXiv parse error: {str(e)}")
            return []


class PubMedMCP:
    """PubMed API integration for medical/biological research"""
    
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.enabled = os.getenv("ENABLE_PUBMED", "true").lower() == "true"
    
    async def search_articles(self, query: str, max_results: int = 5) -> List[Source]:
        """Search PubMed articles"""
        if not self.enabled:
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                # Search for article IDs
                search_response = await client.get(
                    f"{self.base_url}/esearch.fcgi",
                    params={
                        "db": "pubmed",
                        "term": query,
                        "retmax": max_results,
                        "retmode": "json"
                    },
                    timeout=10.0
                )
                
                if search_response.status_code != 200:
                    return []
                
                ids = search_response.json()["esearchresult"]["idlist"]
                
                if not ids:
                    return []
                
                # Fetch article details
                fetch_response = await client.get(
                    f"{self.base_url}/esummary.fcgi",
                    params={
                        "db": "pubmed",
                        "id": ",".join(ids),
                        "retmode": "json"
                    },
                    timeout=10.0
                )
                
                if fetch_response.status_code == 200:
                    return self._parse_pubmed_response(fetch_response.json())
        except Exception as e:
            print(f"PubMed search error: {str(e)}")
        
        return []
    
    def _parse_pubmed_response(self, data: dict) -> List[Source]:
        """Parse PubMed JSON response"""
        try:
            result = data.get("result", {})
            sources = []
            
            for pmid, article in result.items():
                if pmid == "uids":
                    continue
                
                title = article.get("title", "")
                authors = article.get("authors", [])
                author_str = ", ".join([a.get("name", "") for a in authors[:3]])
                if len(authors) > 3:
                    author_str += " et al."
                
                # Get abstract (if available)
                source_info = article.get("source", "")
                pub_date = article.get("pubdate", "")
                
                snippet = f"{source_info} ({pub_date})"
                url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                
                source = Source(
                    title=f"{title} - {author_str}",
                    url=url,
                    snippet=snippet,
                    relevance_score=0.9,
                    source_type="pubmed",
                    content=f"Title: {title}\nAuthors: {author_str}\nSource: {source_info}\nPubMed ID: {pmid}"
                )
                sources.append(source)
            
            return sources
        except Exception as e:
            print(f"PubMed parse error: {str(e)}")
            return []


class MCPIntegrations:
    """Unified MCP integrations service"""
    
    def __init__(self):
        self.github = GitHubMCP()
        self.arxiv = ArXivMCP()
        self.pubmed = PubMedMCP()
    
    async def search_all(self, query: str, max_per_source: int = 3) -> List[Source]:
        """Search all MCP sources"""
        import asyncio
        
        # Run all searches concurrently
        results = await asyncio.gather(
            self.github.search_repositories(query, max_per_source),
            self.arxiv.search_papers(query, max_per_source),
            self.pubmed.search_articles(query, max_per_source),
            return_exceptions=True
        )
        
        # Combine results
        all_sources = []
        for result in results:
            if isinstance(result, list):
                all_sources.extend(result)
        
        return all_sources
