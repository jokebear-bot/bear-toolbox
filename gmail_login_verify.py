#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📧 Gmail 登录测试（带验证处理）
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stealth_browser import StealthBrowser

# 用户提供的账号
EMAIL = "your_email@gmail.com"
PASSWORD = "YOUR_PASSWORD_HERE"

async def login_gmail():
    """登录 Gmail"""
    print("=" * 60)
    print("📧 Gmail 登录")
    print("=" * 60)
    
    async with StealthBrowser(headless=False) as browser:  # 非 headless 便于调试
        print("\n🚀 正在打开 Gmail...")
        
        # 访问 Gmail
        await browser.goto("https://mail.google.com", wait_for="body")
        await asyncio.sleep(3)
        
        print(f"📄 当前 URL: {browser.page.url}")
        
        # 检查是否需要验证
        current_url = browser.page.url
        if "challenge" in current_url or "signinchooser" in current_url:
            print("⚠️ 检测到验证页面，等待用户确认...")
            print("请手动点击 'Yes, it was me' 按钮")
            await asyncio.sleep(10)  # 给用户时间手动确认
            
        # 检查是否已经登录
        if "inbox" in current_url or "mail.google.com/mail" in current_url:
            print("✅ 检测到已登录状态！")
            await asyncio.sleep(2)
            screenshot_final = "/tmp/gmail_inbox.png"
            await browser.screenshot(screenshot_final)
            print(f"📸 收件箱截图: {screenshot_final}")
            
            # 获取邮件列表
            print("\n📨 获取邮件列表...")
            await asyncio.sleep(2)
            
            # 截图看邮件
            screenshot_emails = "/tmp/gmail_emails.png"
            await browser.screenshot(screenshot_emails, full_page=True)
            print(f"📸 邮件列表: {screenshot_emails}")
            return
        
        # 需要重新登录
        print("\n🔍 查找邮箱输入框...")
        
        email_selectors = [
            'input[type="email"]',
            '#identifierId',
            'input[name="identifier"]',
        ]
        
        email_filled = False
        for selector in email_selectors:
            try:
                await browser.page.fill(selector, EMAIL, timeout=3000)
                print(f"✅ 已输入邮箱")
                email_filled = True
                break
            except:
                continue
        
        if email_filled:
            # 点击下一步
            await asyncio.sleep(1)
            try:
                await browser.page.click('button:has-text("Next")', timeout=3000)
                print("✅ 点击下一步")
            except:
                try:
                    await browser.page.click('#identifierNext', timeout=3000)
                    print("✅ 点击下一步")
                except:
                    pass
            
            # 等待密码页面
            await asyncio.sleep(3)
            
            # 输入密码
            print("\n🔍 输入密码...")
            try:
                await browser.page.fill('input[type="password"]', PASSWORD, timeout=5000)
                print("✅ 已输入密码")
                
                # 点击登录
                await asyncio.sleep(1)
                await browser.page.click('button:has-text("Next")', timeout=3000)
                print("✅ 点击登录")
                
                # 等待处理
                await asyncio.sleep(5)
                
                # 检查是否需要验证
                current_url = browser.page.url
                print(f"\n📄 当前 URL: {current_url}")
                
                if "challenge" in current_url:
                    print("⚠️ 需要验证！请手动点击确认...")
                    await asyncio.sleep(15)  # 等待手动确认
                    
                    # 再次截图
                    screenshot_verify = "/tmp/gmail_after_verify.png"
                    await browser.screenshot(screenshot_verify)
                    print(f"📸 验证后页面: {screenshot_verify}")
                
            except Exception as e:
                print(f"❌ 密码输入失败: {e}")
        
        # 最终截图
        await asyncio.sleep(3)
        screenshot_final = "/tmp/gmail_final.png"
        await browser.screenshot(screenshot_final, full_page=True)
        print(f"\n📸 最终页面: {screenshot_final}")
        
    print("\n" + "=" * 60)
    print("✅ 完成")
    print("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(login_gmail())
    except KeyboardInterrupt:
        print("\n👋 已退出")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
