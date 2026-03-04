#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📧 Gmail 登录测试
登录用户提供的 Gmail 账号
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
    
    async with StealthBrowser(headless=True) as browser:
        print("\n🚀 正在打开 Gmail...")
        
        # 访问 Gmail
        await browser.goto("https://mail.google.com", wait_for="body")
        await asyncio.sleep(2)
        
        print("✅ Gmail 页面已加载")
        
        # 保存初始页面截图
        screenshot1 = "/tmp/gmail_step1.png"
        await browser.screenshot(screenshot1)
        print(f"📸 初始页面: {screenshot1}")
        
        # 检查是否已经登录
        current_url = browser.page.url
        if "inbox" in current_url or "mail" in current_url.split("/")[-1]:
            print("✅ 检测到已登录状态！")
            await asyncio.sleep(2)
            screenshot_final = "/tmp/gmail_inbox.png"
            await browser.screenshot(screenshot_final)
            print(f"📸 收件箱截图: {screenshot_final}")
            return
        
        # 查找邮箱输入框
        print("\n🔍 查找邮箱输入框...")
        try:
            # 尝试多种选择器
            email_selectors = [
                'input[type="email"]',
                '#identifierId',
                'input[name="identifier"]',
                '[id*="email"]',
            ]
            
            email_filled = False
            for selector in email_selectors:
                try:
                    await browser.page.fill(selector, EMAIL, timeout=3000)
                    print(f"✅ 已输入邮箱: {selector}")
                    email_filled = True
                    break
                except:
                    continue
            
            if not email_filled:
                print("❌ 无法找到邮箱输入框")
                return
            
            # 点击下一步
            await asyncio.sleep(1)
            next_selectors = [
                '#identifierNext',
                'button:has-text("Next")',
                'button:has-text("下一步")',
                '[id*="next"]',
            ]
            
            for selector in next_selectors:
                try:
                    await browser.page.click(selector, timeout=3000)
                    print(f"✅ 点击下一步: {selector}")
                    break
                except:
                    continue
            
            # 等待密码页面
            print("\n⏳ 等待密码输入页面...")
            await asyncio.sleep(3)
            
            # 保存中间截图
            screenshot2 = "/tmp/gmail_step2_password.png"
            await browser.screenshot(screenshot2)
            print(f"📸 密码页面: {screenshot2}")
            
            # 输入密码
            print("\n🔍 查找密码输入框...")
            password_selectors = [
                'input[type="password"]',
                '[name="password"]',
                '[id*="password"]',
            ]
            
            password_filled = False
            for selector in password_selectors:
                try:
                    await browser.page.fill(selector, PASSWORD, timeout=3000)
                    print(f"✅ 已输入密码: {selector}")
                    password_filled = True
                    break
                except:
                    continue
            
            if not password_filled:
                print("❌ 无法找到密码输入框")
                return
            
            # 点击登录
            await asyncio.sleep(1)
            login_selectors = [
                '#passwordNext',
                'button:has-text("Next")',
                'button:has-text("登录")',
                '[id*="next"]',
            ]
            
            for selector in login_selectors:
                try:
                    await browser.page.click(selector, timeout=3000)
                    print(f"✅ 点击登录: {selector}")
                    break
                except:
                    continue
            
            # 等待登录完成
            print("\n⏳ 等待登录完成...")
            await asyncio.sleep(5)
            
            # 检查是否成功
            current_url = browser.page.url
            print(f"\n📄 当前 URL: {current_url}")
            
            if "inbox" in current_url or "mail" in current_url:
                print("✅ 登录成功！")
                screenshot_final = "/tmp/gmail_inbox.png"
                await browser.screenshot(screenshot_final)
                print(f"📸 收件箱截图: {screenshot_final}")
                
                # 检查未读邮件数量
                unread = await browser.page.evaluate("""
                    () => {
                        const badges = document.querySelectorAll('[data-tooltip="Inbox"] .bsU, .aio');
                        return badges.length;
                    }
                """)
                print(f"📨 检测到未读邮件元素: {unread}")
                
            elif "challenge" in current_url or "recovery" in current_url:
                print("⚠️ 需要验证（可能是新设备登录验证）")
                screenshot_verify = "/tmp/gmail_verify.png"
                await browser.screenshot(screenshot_verify)
                print(f"📸 验证页面: {screenshot_verify}")
                
            else:
                print("⚠️ 登录状态未知，请查看截图")
                screenshot_unknown = "/tmp/gmail_unknown.png"
                await browser.screenshot(screenshot_unknown)
                print(f"📸 当前页面: {screenshot_unknown}")
        
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            import traceback
            traceback.print_exc()
        
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
