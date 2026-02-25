#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 实用搜索工具
提供多种搜索方案，绕过反爬限制
"""

import requests
import json
from typing import List, Dict, Optional
import os
import sys

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anti_spider_tools import get_random_headers

# 代理设置
PROXIES = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

class BraveSearch:
    """
    Brave Search API (推荐)
    需要 API Key，但稳定可靠
    免费额度：2000 queries/month
    注册: https://api.search.brave.com/
    """
    
    API_URL = "https://api.search.brave.com/res/v1/web/search"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("BRAVE_API_KEY")
    
    def search(self, query: str, count: int = 10) -> List[Dict]:
        """搜索"""
        if not self.api_key:
            print("⚠️ 未设置 BRAVE_API_KEY，跳过 Brave Search")
            return []
        
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key,
        }
        
        params = {
            "q": query,
            "count": min(count, 20),
            "search_lang": "zh",
        }
        
        try:
            response = requests.get(
                self.API_URL,
                headers=headers,
                params=params,
                proxies=PROXIES,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get("web", {}).get("results", []):
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "description": item.get("description", ""),
                    })
                return results
            else:
                print(f"❌ Brave API 错误: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Brave 搜索失败: {e}")
            return []

class SerperSearch:
    """
    Serper.dev - Google Search API
    需要 API Key
    免费额度：2500 queries
    注册: https://serper.dev/
    """
    
    API_URL = "https://google.serper.dev/search"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("SERPER_API_KEY")
    
    def search(self, query: str, count: int = 10) -> List[Dict]:
        """搜索"""
        if not self.api_key:
            return []
        
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }
        
        payload = {
            "q": query,
            "num": min(count, 10),
        }
        
        try:
            response = requests.post(
                self.API_URL,
                headers=headers,
                json=payload,
                proxies=PROXIES,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get("organic", []):
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("link", ""),
                        "description": item.get("snippet", ""),
                    })
                return results
            else:
                return []
                
        except Exception as e:
            print(f"❌ Serper 搜索失败: {e}")
            return []

class WikipediaSearch:
    """
    Wikipedia API - 无需 Key，知识查询
    """
    
    API_URL = "https://zh.wikipedia.org/w/api.php"
    
    def search(self, query: str, count: int = 10) -> List[Dict]:
        """搜索 Wikipedia"""
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": count,
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        try:
            response = requests.get(
                self.API_URL,
                params=params,
                headers=headers,
                proxies=PROXIES,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get("query", {}).get("search", []):
                    title = item.get("title", "")
                    results.append({
                        "title": title,
                        "url": f"https://zh.wikipedia.org/wiki/{title.replace(' ', '_')}",
                        "description": item.get("snippet", "").replace("<span class='searchmatch'>", "**").replace("</span>", "**"),
                    })
                return results
            return []
            
        except Exception as e:
            print(f"❌ Wikipedia 搜索失败: {e}")
            return []

class WebFetch:
    """
    网页内容抓取（带反爬伪装）
    """
    
    def fetch(self, url: str) -> Optional[str]:
        """抓取网页内容"""
        try:
            headers = get_random_headers()
            headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            
            response = requests.get(
                url,
                headers=headers,
                proxies=PROXIES,
                timeout=20,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                return response.text
            else:
                print(f"⚠️ HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 抓取失败: {e}")
            return None

class UnifiedSearch:
    """
    统一搜索接口 - 自动选择可用的搜索源
    """
    
    def __init__(self):
        self.engines = {
            "brave": BraveSearch(),
            "serper": SerperSearch(),
            "wikipedia": WikipediaSearch(),
        }
        self.fetcher = WebFetch()
    
    def search(self, query: str, count: int = 10) -> Dict[str, List[Dict]]:
        """
        使用所有可用引擎搜索
        
        Returns:
            {引擎名: 结果列表}
        """
        results = {}
        
        for name, engine in self.engines.items():
            try:
                r = engine.search(query, count)
                if r:
                    results[name] = r
                    print(f"✅ {name}: {len(r)} 条结果")
                else:
                    print(f"⚠️ {name}: 无结果")
            except Exception as e:
                print(f"❌ {name}: {e}")
        
        return results
    
    def fetch_article(self, url: str) -> Optional[str]:
        """抓取文章内容"""
        return self.fetcher.fetch(url)


def demo():
    """演示"""
    print("🔍 实用搜索工具演示\n")
    print("=" * 60)
    
    searcher = UnifiedSearch()
    
    # 测试 Wikipedia（不需要 API Key）
    print("\n📚 Wikipedia 搜索: 'gold'\n")
    wiki = WikipediaSearch()
    results = wiki.search("gold", count=5)
    
    for i, item in enumerate(results, 1):
        print(f"{i}. {item['title']}")
        print(f"   {item['url']}")
        print()
    
    print("=" * 60)
    print("\n💡 要启用更多搜索源，请设置环境变量:")
    print("  export BRAVE_API_KEY=your_key_here")
    print("  export SERPER_API_KEY=your_key_here")
    print("\n  Brave Search: https://api.search.brave.com/")
    print("  Serper.dev: https://serper.dev/")

if __name__ == "__main__":
    demo()
