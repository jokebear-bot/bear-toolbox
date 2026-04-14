#!/usr/bin/env python3
"""
FT (Financial Times) RSS 新闻获取器
支持获取首页头条新闻
"""

import argparse
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# FT RSS 源
FT_RSS_FEEDS = {
    "home": "https://www.ft.com/rss/home",
    "world": "https://www.ft.com/rss/world",
    "us": "https://www.ft.com/rss/world/us",
    "china": "https://www.ft.com/rss/world/china",
    "markets": "https://www.ft.com/rss/markets",
    "technology": "https://www.ft.com/rss/technology",
}

def fetch_rss(url, proxy=None):
    """获取RSS内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    if proxy:
        proxy_handler = urllib.request.ProxyHandler({
            'http': proxy,
            'https': proxy
        })
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read()
    except Exception as e:
        print(f"Error fetching RSS: {e}", file=sys.stderr)
        return None

def parse_rss(xml_content):
    """解析RSS XML内容"""
    if not xml_content:
        return []
    
    try:
        root = ET.fromstring(xml_content)
        
        # 处理RSS 2.0格式
        items = []
        for item in root.findall('.//item'):
            title = item.find('title')
            link = item.find('link')
            description = item.find('description')
            pub_date = item.find('pubDate')
            
            items.append({
                'title': title.text if title is not None else 'N/A',
                'link': link.text if link is not None else '',
                'description': description.text if description is not None else '',
                'pub_date': pub_date.text if pub_date is not None else ''
            })
        
        return items
    except Exception as e:
        print(f"Error parsing RSS: {e}", file=sys.stderr)
        return []

def format_output(items, format_type='text', limit=5):
    """格式化输出"""
    items = items[:limit]
    
    if format_type == 'qq':
        lines = ["📰 FT 今日头条"]
        lines.append("")
        for i, item in enumerate(items, 1):
            lines.append(f"{i}. {item['title']}")
            if item['link']:
                lines.append(f"   {item['link']}")
            lines.append("")
        return "\n".join(lines)
    
    elif format_type == 'markdown':
        lines = ["# FT 今日头条\n"]
        for item in items:
            lines.append(f"## {item['title']}")
            lines.append(f"- 链接: {item['link']}")
            if item['pub_date']:
                lines.append(f"- 发布时间: {item['pub_date']}")
            if item['description']:
                desc = item['description'][:200] + "..." if len(item['description']) > 200 else item['description']
                lines.append(f"- 摘要: {desc}")
            lines.append("")
        return "\n".join(lines)
    
    else:  # text
        lines = ["FT 今日头条", "=" * 50]
        for item in items:
            lines.append(f"\n标题: {item['title']}")
            lines.append(f"链接: {item['link']}")
            if item['pub_date']:
                lines.append(f"时间: {item['pub_date']}")
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description='FT RSS 新闻获取器')
    parser.add_argument('--source', default='home', choices=list(FT_RSS_FEEDS.keys()),
                        help='RSS源类型')
    parser.add_argument('--limit', type=int, default=5,
                        help='获取新闻数量')
    parser.add_argument('--format', default='text', choices=['text', 'markdown', 'qq'],
                        help='输出格式')
    parser.add_argument('--proxy', default=None,
                        help='代理服务器地址')
    
    args = parser.parse_args()
    
    # 从环境变量获取代理
    proxy = args.proxy or os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy') or 'http://127.0.0.1:7890'
    
    url = FT_RSS_FEEDS.get(args.source, FT_RSS_FEEDS['home'])
    
    xml_content = fetch_rss(url, proxy)
    if not xml_content:
        print("无法获取RSS内容，请检查网络连接", file=sys.stderr)
        sys.exit(1)
    
    items = parse_rss(xml_content)
    if not items:
        print("无法解析RSS内容", file=sys.stderr)
        sys.exit(1)
    
    output = format_output(items, args.format, args.limit)
    print(output)

if __name__ == '__main__':
    import os
    main()
