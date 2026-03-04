#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐙 GitHub 登录 - 简化版
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stealth_browser import StealthBrowser

GMAIL = "your_email@gmail.com"
PASSWORD = "YOUR_PASSWORD_HERE"

async def simple_github_login():
    """简化版 GitHub 登录"""
    print("=" * 60)
    print("🐙 GitHub 登录（简化版）")
    print("=" * 60)
    
    async with StealthBrowser(headless=True) as browser:
        # 直接访问 Google OAuth URL for GitHub
        print("\n🚀 直接访问 Google 授权页面...")
        
        oauth_url = "https://accounts.google.com/o/oauth2/auth?client_id=1078992815106-brpsupgvhheqg35tupphbh0qk9c32nq8.apps.googleusercontent.com&redirect_uri=https://github.com/sessions/social/google/callback&response_type=code&scope=openid email profile"
        
        await browser.goto(oauth_url, wait_for="body")
        await asyncio.sleep(3)
        
        print(f"📄 当前 URL: {browser.page.url[:60]}...")
        
        screenshot1 = "/tmp/gh_simple_step1.png"
        await browser.screenshot(screenshot1)
        print(f"📸 截图: {screenshot1}")
        
        # 检查页面内容
        page_content = await browser.page.content()
        
        if "identifier" in browser.page.url or "signin" in browser.page.url:
            print("\n✅ 检测到登录页面")
            
            # 输入邮箱
            try:
                await browser.page.fill('input[type="email"]', GMAIL)
                print(f"✅ 输入邮箱: {GMAIL}")
                
                await asyncio.sleep(1)
                
                # 查找并点击下一步
                await browser.page.press('input[type="email"]', 'Enter')
                print("✅ 按回车提交邮箱")
                
                await asyncio.sleep(4)
                
                screenshot2 = "/tmp/gh_simple_step2.png"
                await browser.screenshot(screenshot2)
                print(f"📸 截图: {screenshot2}")
                
                # 输入密码
                await browser.page.fill('input[type="password"]', PASSWORD)
                print("✅ 输入密码")
                
                await asyncio.sleep(1)
                
                # 提交密码
                await browser.page.press('input[type="password"]', 'Enter')
                print("✅ 按回车提交密码")
                
                await asyncio.sleep(5)
                
                screenshot3 = "/tmp/gh_simple_step3.png"
                await browser.screenshot(screenshot3)
                print(f"📸 截图: {screenshot3}")
                
                # 检查结果
                current_url = browser.page.url
                print(f"\n📄 最终 URL: {current_url}")
                
                if "github" in current_url and "google" not in current_url:
                    print("✅ 看起来已跳转到 GitHub！")
                    
                    # 获取 cookies
                    cookies = await browser.context.cookies()
                    github_cookies = [c for c in cookies if 'github' in c['domain']]
                    if github_cookies:
                        print(f"\n🍪 获取到 {len(github_cookies)} 个 GitHub cookies")
                        cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in github_cookies])
                        print(f"Cookie: {cookie_str[:150]}...")
                else:
                    print("⚠️ 可能需要额外验证")
                    
            except Exception as e:
                print(f"❌ 错误: {e}")
        else:
            print("⚠️ 未检测到登录页面")
        
    print("\n" + "=" * 60)
    print("✅ 完成")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(simple_github_login())
