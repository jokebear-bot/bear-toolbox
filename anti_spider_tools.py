#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🕷️ 反爬虫绕过工具集
提供多种方式绕过常见的反爬机制
"""

import requests
import random
import time
import json
from urllib.parse import urlencode, urlparse
from typing import Optional, Dict, List

# ============ 1. 浏览器指纹伪装 ============

USER_AGENTS = [
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    # Chrome Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Safari Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0 Edg/120.0.0.0",
    # Mobile
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
]

ACCEPT_HEADERS = {
    "html": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "json": "application/json,text/plain,*/*",
    "api": "application/json, text/javascript, */*; q=0.01",
}

LANGUAGES = [
    "zh-CN,zh;q=0.9,en;q=0.8",
    "en-US,en;q=0.9,zh-CN;q=0.8",
    "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
]

def get_random_headers(accept_type: str = "html", referer: str = None) -> Dict[str, str]:
    """生成随机请求头"""
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": ACCEPT_HEADERS.get(accept_type, ACCEPT_HEADERS["html"]),
        "Accept-Language": random.choice(LANGUAGES),
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }
    
    if referer:
        headers["Referer"] = referer
    
    return headers

# ============ 2. 代理配置 ============

class ProxyManager:
    """代理管理器"""
    
    def __init__(self):
        self.proxies = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890",
        }
        self.socks_proxies = {
            "http": "socks5://127.0.0.1:7891",
            "https": "socks5://127.0.0.1:7891",
        }
    
    def get_proxy(self, use_socks: bool = False) -> Dict[str, str]:
        return self.socks_proxies if use_socks else self.proxies
    
    def test_proxy(self) -> bool:
        """测试代理是否可用"""
        try:
            response = requests.get(
                "https://www.google.com/robots.txt",
                proxies=self.proxies,
                timeout=5
            )
            return response.status_code == 200
        except:
            return False

# ============ 3. 智能请求类 ============

class StealthRequester:
    """
    智能请求器 - 自动处理反爬
    
    功能：
    - 自动轮换 User-Agent
    - 智能延迟
    - Cookie 持久化
    - 自动重试
    - 代理支持
    """
    
    def __init__(self, use_proxy: bool = True, delay: tuple = (1, 3)):
        self.session = requests.Session()
        self.use_proxy = use_proxy
        self.delay_range = delay
        self.proxy_manager = ProxyManager()
        self.last_request_time = 0
        
        if use_proxy and self.proxy_manager.test_proxy():
            self.session.proxies.update(self.proxy_manager.get_proxy())
    
    def _random_delay(self):
        """随机延迟，模拟人类行为"""
        min_delay, max_delay = self.delay_range
        # 添加 jitter 避免规律性
        delay = random.uniform(min_delay, max_delay)
        # 确保请求间隔
        elapsed = time.time() - self.last_request_time
        if elapsed < delay:
            time.sleep(delay - elapsed)
        self.last_request_time = time.time()
    
    def get(self, url: str, headers: Dict = None, **kwargs) -> requests.Response:
        """智能 GET 请求"""
        self._random_delay()
        
        if headers is None:
            headers = get_random_headers(referer=self._get_referer(url))
        
        try:
            response = self.session.get(url, headers=headers, timeout=15, **kwargs)
            return response
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {e}")
            raise
    
    def post(self, url: str, data=None, json=None, headers: Dict = None, **kwargs) -> requests.Response:
        """智能 POST 请求"""
        self._random_delay()
        
        if headers is None:
            headers = get_random_headers(accept_type="api", referer=self._get_referer(url))
            headers["Content-Type"] = "application/x-www-form-urlencoded" if data else "application/json"
            headers["X-Requested-With"] = "XMLHttpRequest"
        
        try:
            response = self.session.post(url, data=data, json=json, headers=headers, timeout=15, **kwargs)
            return response
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {e}")
            raise
    
    def _get_referer(self, url: str) -> str:
        """生成合理的 Referer"""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}/"
    
    def close(self):
        """关闭会话"""
        self.session.close()

# ============ 4. 特定网站适配器 ============

class XiaohongshuAdapter:
    """
    小红书适配器
    注意：小红书有强力的风控，完全绕过需要更复杂的方案
    """
    
    BASE_URL = "https://www.xiaohongshu.com"
    API_URL = "https://edith.xiaohongshu.com"
    
    def __init__(self, stealth: StealthRequester = None):
        self.stealth = stealth or StealthRequester()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "X-Sign": "",  # 需要动态生成
            "X-Timestamp": str(int(time.time())),
        }
    
    def search_notes(self, keyword: str, page: int = 1):
        """
        搜索笔记
        ⚠️ 小红书 API 需要签名，此示例仅作参考
        """
        url = f"{self.API_URL}/api/sns/web/v1/search/notes"
        params = {
            "keyword": keyword,
            "page": page,
            "page_size": 20,
        }
        
        try:
            response = self.stealth.get(url, headers=self.headers, params=params)
            return response.json()
        except Exception as e:
            print(f"❌ 小红书搜索失败: {e}")
            return None

class FinancialTimesAdapter:
    """Financial Times 适配器"""
    
    def __init__(self, stealth: StealthRequester = None):
        self.stealth = stealth or StealthRequester()
    
    def get_article(self, url: str) -> Optional[str]:
        """获取文章内容"""
        try:
            headers = get_random_headers()
            headers["Referer"] = "https://www.ft.com/"
            
            response = self.stealth.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.text
            elif response.status_code == 403:
                print("❌ FT 返回 403 - 可能需要订阅或更强的伪装")
                return None
            else:
                print(f"❌ FT 返回 {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 获取 FT 文章失败: {e}")
            return None

class DuckDuckGoAdapter:
    """DuckDuckGo 搜索适配器"""
    
    def __init__(self, stealth: StealthRequester = None):
        self.stealth = stealth or StealthRequester()
    
    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """搜索"""
        url = "https://html.duckduckgo.com/html/"
        
        headers = get_random_headers()
        headers["Origin"] = "https://html.duckduckgo.com"
        headers["Referer"] = "https://html.duckduckgo.com/"
        
        data = {
            "q": query,
            "kl": "zh-cn",
            "df": "",
        }
        
        try:
            response = self.stealth.post(url, data=data, headers=headers)
            return self._parse_results(response.text, max_results)
        except Exception as e:
            print(f"❌ 搜索失败: {e}")
            return []
    
    def _parse_results(self, html: str, max_results: int) -> List[Dict]:
        """解析搜索结果"""
        import re
        from html import unescape
        
        results = []
        
        # DuckDuckGo HTML 格式 1
        pattern1 = r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern1, html)
        
        # DuckDuckGo HTML 格式 2 (新版)
        pattern2 = r'<a[^>]*rel="nofollow"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
        matches2 = re.findall(pattern2, html)
        matches.extend(matches2)
        
        for i, (link, title) in enumerate(matches[:max_results]):
            # HTML 解码
            title = unescape(title)
            title = title.replace('<b>', '').replace('</b>', '')
            
            results.append({
                "index": i + 1,
                "title": title.strip(),
                "url": link
            })
        
        return results

# ============ 5. 使用示例 ============

def demo():
    """演示用法"""
    print("🕷️ 反爬虫工具演示\n")
    
    # 1. 创建智能请求器
    stealth = StealthRequester(use_proxy=True)
    
    # 2. DuckDuckGo 搜索
    print("🔍 DuckDuckGo 搜索: 'gold price'")
    ddg = DuckDuckGoAdapter(stealth)
    results = ddg.search("gold price", max_results=5)
    
    for item in results:
        print(f"  {item['index']}. {item['title']}")
        print(f"     {item['url']}\n")
    
    # 3. 清理
    stealth.close()
    print("✅ 演示完成")

if __name__ == "__main__":
    demo()
