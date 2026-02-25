#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐙 GitHub 登录测试
使用 Gmail 账号登录 GitHub
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stealth_browser import StealthBrowser

async def login_github():
    """使用 Gmail 登录 GitHub"""
    print("=" * 60)
    print("🐙 GitHub 登录 (使用 Gmail)")
    print("=" * 60)
    
    async with StealthBrowser(headless=True) as browser:
        print("\n🚀 正在打开 GitHub...")
        
        # 访问 GitHub 登录页
        await browser.goto("https://github.com/login", wait_for="body")
        await asyncio.sleep(2)
        
        print("✅ GitHub 登录页已加载")
        
        # 保存初始页面截图
        screenshot1 = "/tmp/github_login.png"
        await browser.screenshot(screenshot1)
        print(f"📸 登录页面: {screenshot1}")
        
        # 查找 Google 登录按钮
        print("\n🔍 查找 Google 登录按钮...")
        google_selectors = [
            'input[value*="Google"]',
            'button:has-text("Google")',
            '[class*="google"]',
            'a[href*="google"]',
            '[data-testid*="google"]',
        ]
        
        google_clicked = False
        for selector in google_selectors:
            try:
                await browser.page.click(selector, timeout=3000)
                print(f"✅ 点击 Google 登录: {selector}")
                google_clicked = True
                break
            except:
                continue
        
        if not google_clicked:
            print("⚠️ 未找到 Google 按钮，尝试查找其他第三方登录...")
            # 查找所有按钮并打印文本
            buttons = await browser.page.evaluate("""
                () => Array.from(document.querySelectorAll('button, a, input[type="submit"]'))
                    .map(el => ({ tag: el.tagName, text: el.innerText || el.value, class: el.className }))
                    .filter(item => item.text && item.text.length < 50)
            """)
            print("\n找到的按钮/链接:")
            for btn in buttons[:10]:
                print(f"  {btn['tag']}: {btn['text'][:30]}")
        
        if google_clicked:
            # 等待 Google 登录弹窗或跳转
            print("\n⏳ 等待 Google 登录流程...")
            await asyncio.sleep(5)
            
            # 保存中间截图
            screenshot2 = "/tmp/github_google_auth.png"
            await browser.screenshot(screenshot2)
            print(f"📸 Google 认证页面: {screenshot2}")
            
            # 检查是否需要选择账号
            current_url = browser.page.url
            print(f"\n📄 当前 URL: {current_url}")
            
            if "accounts.google.com" in current_url:
                print("✅ 进入 Google 账号选择页面")
                
                # 查找账号
                account_selectors = [
                    '[data-email="jokebearbot@gmail.com"]',
                    '[id*="jokebearbot"]',
                    'div:has-text("jokebearbot")',
                ]
                
                for selector in account_selectors:
                    try:
                        await browser.page.click(selector, timeout=3000)
                        print(f"✅ 选择账号: {selector}")
                        break
                    except:
                        continue
                
                await asyncio.sleep(5)
            
            # 检查登录结果
            current_url = browser.page.url
            print(f"\n📄 最终 URL: {current_url}")
            
            if "github.com" in current_url and ("dashboard" in current_url or "github.com" == current_url.replace("https://", "").strip("/")):
                print("✅ GitHub 登录成功！")
                screenshot_final = "/tmp/github_dashboard.png"
                await browser.screenshot(screenshot_final)
                print(f"📸 Dashboard: {screenshot_final}")
                
                # 获取用户名
                username = await browser.page.evaluate("""
                    () => {
                        const el = document.querySelector('[class*="avatar"] img, [data-testid="avatar"]');
                        return el?.alt || el?.title || '';
                    }
                """)
                if username:
                    print(f"👤 用户名: {username}")
                    
            else:
                print("⚠️ 登录状态未知")
                screenshot_unknown = "/tmp/github_status.png"
                await browser.screenshot(screenshot_unknown)
                print(f"📸 当前页面: {screenshot_unknown}")
        
    print("\n" + "=" * 60)
    print("✅ 完成")
    print("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(login_github())
    except KeyboardInterrupt:
        print("\n👋 已退出")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
