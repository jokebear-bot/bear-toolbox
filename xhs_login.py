#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📱 小红书登录助手 - Playwright 版
打开小红书网页版并获取登录二维码
"""

import asyncio
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stealth_browser import StealthBrowser

async def login_xiaohongshu():
    """打开小红书并获取登录二维码"""
    print("=" * 60)
    print("📱 小红书登录助手")
    print("=" * 60)
    
    async with StealthBrowser(headless=False) as browser:
        print("\n🚀 正在打开小红书...")
        
        # 访问小红书
        await browser.goto("https://www.xiaohongshu.com", wait_for="body")
        print("✅ 小红书主页已加载")
        
        # 等待页面完全加载
        await asyncio.sleep(2)
        
        # 查找登录按钮并点击
        try:
            # 尝试多种方式找到登录入口
            login_selectors = [
                'a[href="/login"]',
                '.login-btn',
                'button:has-text("登录")',
                'a:has-text("登录")',
                '[class*="login"]',
            ]
            
            for selector in login_selectors:
                try:
                    await browser.page.click(selector, timeout=3000)
                    print(f"✅ 点击登录按钮: {selector}")
                    break
                except:
                    continue
            else:
                print("ℹ️ 未找到登录按钮，可能已经显示二维码")
                
        except Exception as e:
            print(f"ℹ️ 登录按钮处理: {e}")
        
        # 等待二维码出现
        print("\n⏳ 等待二维码加载...")
        await asyncio.sleep(3)
        
        # 查找二维码
        qr_selectors = [
            'img[src*="qrcode"]',
            '.qrcode img',
            '[class*="qr"] img',
            'canvas',
        ]
        
        qr_found = False
        for selector in qr_selectors:
            try:
                element = await browser.page.query_selector(selector)
                if element:
                    print(f"✅ 找到二维码元素: {selector}")
                    qr_found = True
                    break
            except:
                continue
        
        if not qr_found:
            print("⚠️ 未自动检测到二维码，请查看浏览器窗口")
        
        # 截图保存
        screenshot_path = "/tmp/xiaohongshu_login.png"
        await browser.screenshot(screenshot_path)
        print(f"\n📸 已保存页面截图: {screenshot_path}")
        
        # 打印页面信息
        print("\n📄 当前页面信息:")
        print(f"   URL: {browser.page.url}")
        
        # 等待用户扫码
        print("\n" + "=" * 60)
        print("⏳ 请扫码登录")
        print("=" * 60)
        print("请在打开的浏览器窗口中扫描二维码")
        print("登录完成后，按 Ctrl+C 结束程序")
        print("=" * 60 + "\n")
        
        # 保持运行直到用户中断
        try:
            while True:
                await asyncio.sleep(1)
                # 检查是否已登录（URL 变化或出现用户头像）
                current_url = browser.page.url
                if "/explore" in current_url or "/user" in current_url:
                    print("✅ 检测到登录成功！")
                    break
        except KeyboardInterrupt:
            print("\n\n👋 用户中断")
        
        # 保存最终状态
        final_screenshot = "/tmp/xiaohongshu_final.png"
        await browser.screenshot(final_screenshot)
        print(f"📸 最终状态截图: {final_screenshot}")
        
    print("\n✅ 程序结束")

if __name__ == "__main__":
    try:
        asyncio.run(login_xiaohongshu())
    except KeyboardInterrupt:
        print("\n👋 已退出")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
