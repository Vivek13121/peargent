"""
Web Search Tool for Peargent
Queries search engines (DuckDuckGo) for up-to-date information and retrieves results.
"""

from typing import Dict, Any, Optional, List
from urllib.parse import quote

from peargent import Tool

try:
    import requests
except ImportError:
    requests = None


def web_search(
    query: str,
    max_results: int = 5,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    time_range: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search the web using DuckDuckGo and retrieve search results.
    
    Provides:
    - Search result titles and snippets
    - URLs for each result
    - Source metadata
    - Safe search filtering
    - Regional and time-based filtering
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 5, max: 25)
        region: Region code for localized results (default: "wt-wt" for worldwide)
                Examples: "us-en" (US English), "uk-en" (UK English), "de-de" (Germany)
        safesearch: Safe search level - "strict", "moderate", or "off" (default: "moderate")
        time_range: Filter by time - "d" (day), "w" (week), "m" (month), "y" (year), None (all time)
        
    Returns:
        Dictionary containing:
            - results: List of search results with title, snippet, url
            - metadata: Dict with query info, result count, search engine
            - success: Boolean indicating success
            - error: Error message if any
            
    Example:
        >>> result = web_search("Python programming tutorials")
        >>> for r in result["results"]:
        ...     print(f"{r['title']}: {r['url']}")
        ...     print(r['snippet'])
    """
    if requests is None:
        return {
            "results": [],
            "metadata": {},
            "success": False,
            "error": (
                "requests library is required for web search. "
                "Install it with: pip install requests"
            )
        }
    
    # Validate parameters
    if not query or not query.strip():
        return {
            "results": [],
            "metadata": {},
            "success": False,
            "error": "Query cannot be empty"
        }
    
    # Limit max_results
    max_results = min(max(1, max_results), 25)
    
    # Validate safesearch
    if safesearch not in ["strict", "moderate", "off"]:
        safesearch = "moderate"
    
    # Validate time_range
    if time_range and time_range not in ["d", "w", "m", "y"]:
        time_range = None
    
    try:
        # Use DuckDuckGo HTML search
        results = _search_duckduckgo(query, max_results, region, safesearch, time_range)
        
        if not results:
            return {
                "results": [],
                "metadata": {
                    "query": query,
                    "result_count": 0,
                    "search_engine": "DuckDuckGo",
                    "message": "No results found for your query"
                },
                "success": True,
                "error": None
            }
        
        # Build metadata
        metadata = {
            "query": query,
            "result_count": len(results),
            "search_engine": "DuckDuckGo",
            "region": region,
            "safesearch": safesearch
        }
        
        if time_range:
            metadata["time_range"] = time_range
        
        return {
            "results": results,
            "metadata": metadata,
            "success": True,
            "error": None
        }
        
    except Exception as e:
        # Handle different request exceptions
        error_type = type(e).__name__
        if "Timeout" in error_type:
            error_msg = "Request timed out. Please try again."
        elif "RequestException" in error_type or "ConnectionError" in error_type:
            error_msg = f"Network error: {str(e)}"
        else:
            error_msg = f"Unexpected error: {str(e)}"
        
        return {
            "results": [],
            "metadata": {},
            "success": False,
            "error": error_msg
        }


def _search_duckduckgo(
    query: str,
    max_results: int,
    region: str,
    safesearch: str,
    time_range: Optional[str]
) -> List[Dict[str, str]]:
    """
    Perform search using DuckDuckGo HTML interface.
    
    Returns:
        List of dicts with 'title', 'snippet', 'url' keys
    """
    # DuckDuckGo HTML search endpoint
    base_url = "https://html.duckduckgo.com/html/"
    
    # Map safesearch to DuckDuckGo parameter
    safesearch_map = {
        "strict": "1",
        "moderate": "-1",
        "off": "-2"
    }
    
    # Build search parameters
    params = {
        "q": query,
        "kl": region
    }
    
    # Add safesearch
    if safesearch in safesearch_map:
        params["kp"] = safesearch_map[safesearch]
    
    # Add time range
    if time_range:
        params["df"] = time_range
    
    headers = {
        "User-Agent": "Peargent/0.1 (https://github.com/Peargent/peargent) Python/requests"
    }
    
    try:
        # Send POST request (DuckDuckGo HTML uses POST)
        response = requests.post(base_url, data=params, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Parse HTML response
        results = _parse_duckduckgo_html(response.text, max_results)
        
        return results
        
    except Exception as e:
        raise Exception(f"DuckDuckGo search failed: {str(e)}")


def _parse_duckduckgo_html(html: str, max_results: int) -> List[Dict[str, str]]:
    """
    Parse DuckDuckGo HTML response to extract search results.
    
    Returns:
        List of result dictionaries
    """
    results = []
    
    try:
        # Try to use BeautifulSoup if available
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find all result divs
            result_divs = soup.find_all('div', class_='result')
            
            for div in result_divs[:max_results]:
                # Extract title and URL
                title_link = div.find('a', class_='result__a')
                if not title_link:
                    continue
                
                title = title_link.get_text(strip=True)
                url = title_link.get('href', '')
                
                # Extract snippet
                snippet_div = div.find('a', class_='result__snippet')
                snippet = snippet_div.get_text(strip=True) if snippet_div else ""
                
                if title and url:
                    results.append({
                        "title": title,
                        "snippet": snippet,
                        "url": url
                    })
                
                if len(results) >= max_results:
                    break
        
        except ImportError:
            # Fall back to regex parsing if BeautifulSoup not available
            import re
            
            # Find result blocks using regex
            result_pattern = r'<div class="result[^"]*"[^>]*>.*?</div>\s*</div>'
            result_blocks = re.findall(result_pattern, html, re.DOTALL)
            
            for block in result_blocks[:max_results * 2]:  # Get more to filter
                # Extract title
                title_match = re.search(r'<a[^>]+class="result__a"[^>]*>([^<]+)</a>', block)
                if not title_match:
                    continue
                
                title = title_match.group(1).strip()
                
                # Extract URL
                url_match = re.search(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"', block)
                url = url_match.group(1) if url_match else ""
                
                # Extract snippet
                snippet_match = re.search(r'<a[^>]+class="result__snippet"[^>]*>([^<]+)</a>', block)
                snippet = snippet_match.group(1).strip() if snippet_match else ""
                
                if title and url:
                    results.append({
                        "title": title,
                        "snippet": snippet,
                        "url": url
                    })
                
                if len(results) >= max_results:
                    break
    
    except Exception as e:
        # If parsing fails, return empty list
        pass
    
    return results


class WebSearchTool(Tool):
    """
    Tool for searching the web using DuckDuckGo.
    
    Features:
    - Web search with customizable result count
    - Regional filtering for localized results
    - Safe search filtering
    - Time-based filtering (day, week, month, year)
    - Returns titles, snippets, and URLs
    
    Use cases:
    - Research and information gathering
    - Fact-checking and verification
    - RAG (Retrieval Augmented Generation) applications
    - Real-time information lookup
    - Grounding agent responses with current data
    
    Example:
        >>> from peargent.tools import WebSearchTool
        >>> tool = WebSearchTool()
        >>> result = tool.run({"query": "latest AI developments"})
        >>> for r in result["results"]:
        ...     print(f"{r['title']}: {r['url']}")
    """
    
    def __init__(self):
        super().__init__(
            name="web_search",
            description=(
                "Search the web using DuckDuckGo for up-to-date information. "
                "Returns search results with titles, snippets, and URLs. "
                "Supports filtering by region, safe search level, and time range. "
                "Optional parameters: max_results (int, default: 5, max: 25), "
                "region (str, default: 'wt-wt'), safesearch (str: 'strict'/'moderate'/'off'), "
                "time_range (str: 'd'/'w'/'m'/'y' or None for all time)."
            ),
            input_parameters={
                "query": str
            },
            call_function=web_search
        )


# Create default instance for easy import
websearch_tool = WebSearchTool()
