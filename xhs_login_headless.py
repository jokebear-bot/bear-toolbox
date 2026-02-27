#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📱 小红书登录助手 - 无头模式版
自动截取二维码图片给你扫描
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stealth_browser import StealthBrowser

async def login_xiaohongshu():
    """打开小红书并获取登录二维码"""
    print("=" * 60)
    print("📱 小红书登录助手 (无头模式)")
    print("=" * 60)
    
    # 使用无头模式，但会截取二维码图片
    async with StealthBrowser(headless=True) as browser:
        print("\n🚀 正在打开小红书...")
        
        # 访问小红书
        await browser.goto("https://www.xiaohongshu.com", wait_for="body")
        print("✅ 小红书主页已加载")
        await asyncio.sleep(3)
        
        # 保存初始页面截图
        screenshot1 = "/tmp/xhs_step1_home.png"
        await browser.screenshot(screenshot1)
        print(f"📸 已保存首页截图: {screenshot1}")
        
        # 尝试找到并点击登录按钮
        print("\n🔍 查找登录入口...")
        login_clicked = False
        
        try:
            # 尝试点击各种可能的登录按钮
            selectors = [
                'a[href="/login"]',
                '.login-btn',
                'button:has-text("登录")',
                'a:has-text("登录")',
                '[class*="login"]:not([class*="container"])',
                'text=登录',
            ]
            
            for selector in selectors:
                try:
                    # 检查元素是否存在
                    element = await browser.page.query_selector(selector)
                    if element:
                        await element.click(timeout=3000)
                        print(f"✅ 点击登录按钮: {selector}")
                        login_clicked = True
                        await asyncio.sleep(2)
                        break
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"ℹ️ 登录按钮处理: {e}")
        
        if not login_clicked:
            print("ℹ️ 未找到登录按钮，二维码可能已经显示")
        
        # 等待二维码加载
        print("\n⏳ 等待二维码加载...")
        await asyncio.sleep(3)
        
        # 保存带二维码的页面截图
        screenshot2 = "/tmp/xhs_step2_qrcode.png"
        await browser.screenshot(screenshot2)
        print(f"📸 已保存二维码页面截图: {screenshot2}")
        
        # 尝试找到二维码图片并单独截取
        print("\n🔍 尝试提取二维码...")
        qr_selectors = [
            'img[src*="qrcode"]',
            '.qrcode img',
            '[class*="qr"] img',
            'canvas',
            'img[class*="code"]',
        ]
        
        qr_screenshot = None
        for selector in qr_selectors:
            try:
                element = await browser.page.query_selector(selector)
                if element:
                    qr_screenshot = "/tmp/xhs_qrcode_only.png"
                    await element.screenshot(path=qr_screenshot)
                    print(f"✅ 已截取二维码图片: {qr_screenshot}")
                    break
            except Exception as e:
                continue
        
        # 打印当前页面信息
        print("\n📄 当前页面信息:")
        print(f"   URL: {browser.page.url}")
        print(f"   Title: {await browser.page.title()}")
        
        # 检查页面内容
        page_content = await browser.page.content()
        if "qrcode" in page_content.lower() or "二维码" in page_content:
            print("   ✅ 页面包含二维码相关内容")
        
        print("\n" + "=" * 60)
        print("📋 生成的截图文件:")
        print("=" * 60)
        print(f"1. {screenshot1} - 首页")
        print(f"2. {screenshot2} - 登录/二维码页面")
        if qr_screenshot:
            print(f"3. {qr_screenshot} - 二维码特写")
        print("=" * 60)
        
        # 等待一段时间，检查是否登录成功
        print("\n⏳ 等待扫码 (60秒)...")
        for i in range(60):
            await asyncio.sleep(1)
            current_url = browser.page.url
            if "/explore" in current_url or "/user" in current_url or i % 10 == 0:
                # 刷新页面检查状态
                await browser.page.reload()
                await asyncio.sleep(2)
                current_url = browser.page.url
                
            if "/explore" in current_url or "/user" in current_url:
                print("\n✅ 检测到登录成功！")
                final_screenshot = "/tmp/xhs_step3_logged_in.png"
                await browser.screenshot(final_screenshot)
                print(f"📸 已保存登录后截图: {final_screenshot}")
                break
        else:
            print("\n⏰ 等待超时，未检测到登录")
            final_screenshot = "/tmp/xhs_step3_timeout.png"
            await browser.screenshot(final_screenshot)
            print(f"📸 已保存最终截图: {final_screenshot}")
        
    print("\n✅ 程序结束")
    print("\n💡 提示: 请查看 /tmp/xhs_*.png 文件获取二维码")

if __name__ == "__main__":
    try:
        asyncio.run(login_xiaohongshu())
    except KeyboardInterrupt:
        print("\n👋 已退出")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
