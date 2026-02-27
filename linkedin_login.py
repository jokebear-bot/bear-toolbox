#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 LinkedIn 登录助手
打开领英登录页面
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stealth_browser import StealthBrowser

async def linkedin_login():
    """打开 LinkedIn 登录页面"""
    print("=" * 60)
    print("🔗 LinkedIn 登录助手")
    print("=" * 60)
    
    async with StealthBrowser(headless=True) as browser:
        print("\n🚀 正在打开 LinkedIn 登录页面...")
        
        # 访问领英登录页
        await browser.goto("https://www.linkedin.com/login", wait_for="body")
        await asyncio.sleep(3)
        
        print("✅ 登录页面已加载")
        
        # 保存截图
        screenshot = "/tmp/linkedin_login.png"
        await browser.screenshot(screenshot)
        print(f"📸 已保存截图: {screenshot}")
        
        # 检查页面内容
        page_info = await browser.page.evaluate("""
            () => {
                const usernameField = document.querySelector('#username, input[name="session_key"]');
                const passwordField = document.querySelector('#password, input[name="session_password"]');
                const googleBtn = document.querySelector('[data-id="google-one-tap"]') || 
                                  document.querySelector('button:has-text("Google")');
                
                return {
                    hasUsername: !!usernameField,
                    hasPassword: !!passwordField,
                    hasGoogle: !!googleBtn,
                    url: window.location.href,
                    title: document.title
                };
            }
        """)
        
        print("\n📊 页面元素检测:")
        print(f"   用户名输入框: {'✅' if page_info['hasUsername'] else '❌'}")
        print(f"   密码输入框: {'✅' if page_info['hasPassword'] else '❌'}")
        print(f"   Google登录: {'✅' if page_info['hasGoogle'] else '❌'}")
        print(f"   当前URL: {page_info['url']}")
        
        # 如果跳转到你的档案页面，说明已登录
        if "/in/" in page_info['url']:
            print("\n✅ 检测到已登录状态！")
            profile_screenshot = "/tmp/linkedin_profile_logged_in.png"
            await browser.screenshot(profile_screenshot)
            print(f"📸 档案截图: {profile_screenshot}")
        else:
            print("\n⚠️ 需要登录 - 请查看截图中的登录选项")
            
            # 查找二维码或一键登录选项
            qr_info = await browser.page.evaluate("""
                () => {
                    const qrElements = document.querySelectorAll('[class*="qr"], [class*="qrcode"]');
                    const oneTap = document.querySelector('[id*="google-one-tap"]');
                    
                    return {
                        qrCount: qrElements.length,
                        hasOneTap: !!oneTap
                    };
                }
            """)
            
            if qr_info['qrCount'] > 0:
                print(f"   发现 {qr_info['qrCount']} 个二维码元素")
            if qr_info['hasOneTap']:
                print("   发现 Google One Tap 登录")
        
        # 等待一段时间保持页面
        print("\n⏳ 保持页面 30 秒...")
        await asyncio.sleep(30)
        
    print("\n" + "=" * 60)
    print("✅ 完成")
    print("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(linkedin_login())
    except KeyboardInterrupt:
        print("\n👋 已退出")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
