#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 反爬工具快速测试
一键测试所有反爬方案
"""

import sys
import os

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from anti_spider_tools import StealthRequester, DuckDuckGoAdapter, ProxyManager

def test_basic_proxy():
    """测试基础代理"""
    print("=" * 60)
    print("📡 测试 1: 基础代理连接")
    print("=" * 60)
    
    pm = ProxyManager()
    if pm.test_proxy():
        print("✅ 代理正常 - 可访问 Google")
        return True
    else:
        print("❌ 代理异常 - 请检查 mihomo/clash 是否运行")
        return False

def test_stealth_request():
    """测试智能请求器"""
    print("\n" + "=" * 60)
    print("🕷️ 测试 2: 智能请求器 + DuckDuckGo")
    print("=" * 60)
    
    try:
        stealth = StealthRequester(use_proxy=True)
        ddg = DuckDuckGoAdapter(stealth)
        
        print("🔍 搜索: 'gold price' (带反爬伪装)")
        results = ddg.search("gold price", max_results=5)
        
        if results:
            print(f"✅ 成功! 获取 {len(results)} 条结果:\n")
            for item in results:
                print(f"  {item['index']}. {item['title'][:50]}...")
            return True
        else:
            print("❌ 未获取到结果")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    finally:
        try:
            stealth.close()
        except:
            pass

def test_direct_fetch():
    """测试直接抓取"""
    print("\n" + "=" * 60)
    print("🌐 测试 3: 直接抓取网页")
    print("=" * 60)
    
    test_urls = [
        ("GitHub", "https://github.com/robots.txt"),
        ("StackOverflow", "https://stackoverflow.com/robots.txt"),
    ]
    
    stealth = StealthRequester(use_proxy=True)
    
    for name, url in test_urls:
        try:
            print(f"\n  📥 抓取 {name}...")
            response = stealth.get(url)
            if response.status_code == 200:
                print(f"  ✅ {name} 成功 (HTTP {response.status_code})")
            else:
                print(f"  ⚠️ {name} 返回 HTTP {response.status_code}")
        except Exception as e:
            print(f"  ❌ {name} 失败: {e}")
    
    stealth.close()
    return True

def print_summary():
    """打印使用指南"""
    print("\n" + "=" * 60)
    print("📚 反爬工具使用指南")
    print("=" * 60)
    print("""
1️⃣  基础智能请求 (已可用):
    from anti_spider_tools import StealthRequester
    
    stealth = StealthRequester(use_proxy=True)
    response = stealth.get("https://example.com")
    print(response.text)
    stealth.close()

2️⃣  DuckDuckGo 搜索 (已可用):
    from anti_spider_tools import DuckDuckGoAdapter
    
    ddg = DuckDuckGoAdapter(stealth)
    results = ddg.search("关键词", max_results=10)
    for item in results:
        print(f"{item['title']}: {item['url']}")

3️⃣  高级 Playwright 浏览器 (需安装):
    pip install playwright
    playwright install chromium
    
    python3 stealth_browser.py

4️⃣  代理状态:
    HTTP代理:  127.0.0.1:7890 (Mihomo/Clash)
    SOCKS5:    127.0.0.1:7891
    控制面板:  http://127.0.0.1:9090
    """)

def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════════╗
║           🛡️ 反爬虫工具测试套件                           ║
║           Anti-Spider Bypass Toolkit Test               ║
╚══════════════════════════════════════════════════════════╝
""")
    
    # 运行测试
    results = []
    
    results.append(("代理连接", test_basic_proxy()))
    results.append(("智能请求", test_stealth_request()))
    results.append(("直接抓取", test_direct_fetch()))
    
    # 打印总结
    print("\n" + "=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {status} - {name}")
    
    # 打印使用指南
    print_summary()
    
    # 返回码
    all_passed = all(r[1] for r in results)
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
