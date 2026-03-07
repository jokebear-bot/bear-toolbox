#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎭 Playwright 高级反爬方案 - 简化测试版
"""

import asyncio
from playwright.async_api import async_playwright

async def test_basic():
    """基础测试"""
    print("🚀 启动 Playwright 测试...")
    
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=True)
        print("✅ 浏览器启动成功")
        
        # 创建页面
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        print("✅ 页面创建成功")
        
        # 访问测试页面
        await page.goto("https://httpbin.org/headers")
        content = await page.content()
        print("✅ 页面加载成功")
        print("\n📝 请求头信息:")
        print(content[:1000])
        
        # 关闭
        await browser.close()
        print("\n✅ 测试完成!")

if __name__ == "__main__":
    asyncio.run(test_basic())
