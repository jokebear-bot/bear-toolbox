#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
带代理的 DuckDuckGo 搜索脚本
使用本地 Clash/Mihomo 代理
"""

import requests
import sys
import os

# 代理设置 - 只影响当前脚本，不影响系统其他部分
PROXY_HTTP = "http://127.0.0.1:7890"
PROXY_SOCKS = "socks5://127.0.0.1:7891"

proxies = {
    "http": PROXY_HTTP,
    "https": PROXY_HTTP,
}

def duckduckgo_search(query, max_results=10):
    """使用 DuckDuckGo 搜索（带代理）"""
    try:
        # 使用 DuckDuckGo HTML 版
        url = "https://html.duckduckgo.com/html/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        data = {
            "q": query,
            "kl": "zh-cn"
        }
        
        response = requests.post(
            url, 
            headers=headers, 
            data=data, 
            proxies=proxies,
            timeout=15
        )
        
        results = []
        html = response.text
        
        import re
        pattern = r'<a rel="nofollow" class="result__a" href="([^"]+)">([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        for i, (link, title) in enumerate(matches[:max_results]):
            title = title.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            results.append({
                "index": i + 1,
                "title": title,
                "url": link
            })
        
        return results
        
    except Exception as e:
        return [{"error": str(e)}]

def format_results(results):
    """格式化输出"""
    if not results:
        print("未找到结果")
        return
    
    if "error" in results[0]:
        print(f"❌ 搜索出错: {results[0]['error']}")
        print("\n💡 提示：请确保代理已启动 (mihomo/clash)")
        return
    
    print(f"\n🔍 找到 {len(results)} 个结果:\n")
    print("-" * 70)
    
    for item in results:
        print(f"\n{item['index']}. {item['title']}")
        print(f"   {item['url']}")
    
    print("\n" + "-" * 70)

def test_proxy():
    """测试代理是否可用"""
    try:
        response = requests.get(
            "https://www.google.com/robots.txt",
            proxies=proxies,
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 duck_search_proxy.py '搜索关键词'")
        print("示例: python3 duck_search_proxy.py 'gold price'")
        sys.exit(1)
    
    # 测试代理
    print("🔄 测试代理连接...")
    if not test_proxy():
        print("❌ 代理连接失败")
        print("   请检查 mihomo/clash 是否已启动")
        print(f"   代理地址: {PROXY_HTTP}")
        sys.exit(1)
    
    print("✅ 代理连接成功\n")
    
    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    print(f"🔍 搜索: {query}")
    results = duckduckgo_search(query, max_results)
    format_results(results)
