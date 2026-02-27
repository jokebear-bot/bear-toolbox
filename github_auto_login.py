#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐙 GitHub 自动登录
通过 Google 账号直接登录
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stealth_browser import StealthBrowser

# Gmail 账号信息
GMAIL_EMAIL = "your_email@gmail.com"
GMAIL_PASSWORD = "YOUR_PASSWORD_HERE"

async def auto_login_github():
    """自动登录 GitHub"""
    print("=" * 60)
    print("🐙 GitHub 自动登录")
    print("=" * 60)
    
    async with StealthBrowser(headless=True) as browser:
        # 第1步：打开 GitHub
        print("\n📍 第1步：打开 GitHub 登录页...")
        await browser.goto("https://github.com/login", wait_for="body")
        await asyncio.sleep(2)
        
        screenshot1 = "/tmp/gh_step1_login.png"
        await browser.screenshot(screenshot1)
        print(f"📸 截图: {screenshot1}")
        
        # 第2步：点击 Google 登录按钮
        print("\n📍 第2步：点击 'Sign in with Google'...")
        
        # 查找 Google 按钮
        google_btn = await browser.page.query_selector('input[value*="Google"], button:has-text("Google")')
        if google_btn:
            await google_btn.click()
            print("✅ 点击 Google 登录按钮")
        else:
            # 尝试查找 iframe 中的按钮
            frames = browser.page.frames
            for frame in frames:
                try:
                    btn = await frame.query_selector('[id*="google"]')
                    if btn:
                        await btn.click()
                        print("✅ 在 iframe 中点击 Google 按钮")
                        break
                except:
                    pass
        
        await asyncio.sleep(4)
        
        screenshot2 = "/tmp/gh_step2_google.png"
        await browser.screenshot(screenshot2)
        print(f"📸 截图: {screenshot2}")
        
        current_url = browser.page.url
        print(f"\n📄 当前 URL: {current_url[:80]}...")
        
        # 第3步：在 Google 页面输入邮箱
        if "accounts.google.com" in current_url:
            print("\n📍 第3步：输入 Gmail 邮箱...")
            
            # 等待邮箱输入框
            await asyncio.sleep(2)
            
            # 输入邮箱
            try:
                await browser.page.fill('input[type="email"], #identifierId, input[name="identifier"]', GMAIL_EMAIL)
                print(f"✅ 输入邮箱: {GMAIL_EMAIL}")
            except Exception as e:
                print(f"⚠️ 输入邮箱失败: {e}")
            
            await asyncio.sleep(1)
            
            # 点击下一步
            try:
                await browser.page.click('#identifierNext, button[jsname*="LgbsSe"], button:has-text("Next")')
                print("✅ 点击下一步")
            except Exception as e:
                print(f"⚠️ 点击下一步失败: {e}")
            
            await asyncio.sleep(4)
            
            screenshot3 = "/tmp/gh_step3_password.png"
            await browser.screenshot(screenshot3)
            print(f"📸 截图: {screenshot3}")
            
            # 第4步：输入密码
            print("\n📍 第4步：输入密码...")
            
            try:
                await browser.page.fill('input[type="password"], input[name="password"]', GMAIL_PASSWORD)
                print("✅ 输入密码")
            except Exception as e:
                print(f"⚠️ 输入密码失败: {e}")
            
            await asyncio.sleep(1)
            
            # 点击登录
            try:
                await browser.page.click('#passwordNext, button[jsname*="LgbsSe"], button:has-text("Next")')
                print("✅ 点击登录")
            except Exception as e:
                print(f"⚠️ 点击登录失败: {e}")
            
            await asyncio.sleep(5)
            
            screenshot4 = "/tmp/gh_step4_after_login.png"
            await browser.screenshot(screenshot4)
            print(f"📸 截图: {screenshot4}")
        
        # 第5步：检查结果
        print("\n📍 第5步：检查登录结果...")
        current_url = browser.page.url
        print(f"📄 最终 URL: {current_url}")
        
        if "github.com" in current_url and ("dashboard" in current_url or "/" == current_url.replace("https://github.com", "")):
            print("✅ GitHub 登录成功！")
            
            # 获取用户名
            username = await browser.page.evaluate("""
                () => {
                    const el = document.querySelector('[data-testid="global-profile-menu"] img');
                    return el?.alt || '';
                }
            """)
            if username:
                print(f"👤 用户名: {username}")
        elif "challenge" in current_url or "consent" in current_url:
            print("⚠️ 需要额外验证（可能是新设备或安全验证）")
        else:
            print("⚠️ 登录状态未知")
        
        # 保存 Cookie
        cookies = await browser.context.cookies()
        cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies if 'github' in c['domain']])
        if cookie_str:
            print(f"\n🍪 获取到的 GitHub Cookie:\n{cookie_str[:200]}...")
            with open('/tmp/github_cookies.txt', 'w') as f:
                f.write(cookie_str)
            print("📄 Cookie 已保存到 /tmp/github_cookies.txt")
        
    print("\n" + "=" * 60)
    print("✅ 完成")
    print("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(auto_login_github())
    except KeyboardInterrupt:
        print("\n👋 已退出")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
