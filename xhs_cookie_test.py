#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📱 小红书 Cookie 登录测试
使用用户提供的 Cookie 访问小红书
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stealth_browser import StealthBrowser

# 用户提供的 Cookie
USER_COOKIE = "YOUR_COOKIE_HERE"

async def test_login_with_cookie():
    """使用 Cookie 测试登录状态"""
    print("=" * 60)
    print("📱 小红书 Cookie 登录测试")
    print("=" * 60)
    
    async with StealthBrowser(headless=True) as browser:
        print("\n🚀 正在打开小红书...")
        
        # 先访问主页
        await browser.goto("https://www.xiaohongshu.com", wait_for="body")
        print("✅ 主页已加载")
        
        # 设置 Cookie
        print("\n🍪 正在设置 Cookie...")
        cookies = []
        for item in USER_COOKIE.split(';'):
            item = item.strip()
            if '=' in item:
                name, value = item.split('=', 1)
                cookies.append({
                    'name': name.strip(),
                    'value': value.strip(),
                    'domain': '.xiaohongshu.com',
                    'path': '/'
                })
        
        await browser.context.add_cookies(cookies)
        print(f"✅ 已设置 {len(cookies)} 个 Cookie")
        
        # 刷新页面验证登录
        print("\n🔄 刷新页面验证登录...")
        await browser.page.reload()
        await asyncio.sleep(3)
        
        # 检查登录状态
        print("\n🔍 检查登录状态...")
        current_url = browser.page.url
        print(f"   当前 URL: {current_url}")
        
        # 尝试获取用户信息
        user_info = await browser.page.evaluate("""
            () => {
                // 查找用户头像、昵称等元素
                const avatar = document.querySelector('[class*="avatar"] img, .user-avatar img, img[class*="avatar"]');
                const nickname = document.querySelector('[class*="nickname"], .user-name, [class*="user-name"]');
                const userId = document.querySelector('[class*="user-id"]');
                
                return {
                    hasAvatar: !!avatar,
                    avatarSrc: avatar?.src || '',
                    nickname: nickname?.innerText || '',
                    userId: userId?.innerText || '',
                    pageTitle: document.title,
                    url: window.location.href
                };
            }
        """)
        
        print("\n📊 页面信息:")
        print(f"   页面标题: {user_info['pageTitle']}")
        print(f"   检测到头像: {'✅' if user_info['hasAvatar'] else '❌'}")
        if user_info['nickname']:
            print(f"   昵称: {user_info['nickname']}")
        
        # 保存截图
        screenshot = "/tmp/xhs_cookie_test.png"
        await browser.screenshot(screenshot)
        print(f"\n📸 已保存截图: {screenshot}")
        
        # 测试访问发现页
        print("\n🌐 测试访问发现页...")
        await browser.goto("https://www.xiaohongshu.com/explore", wait_for="body")
        await asyncio.sleep(2)
        
        explore_screenshot = "/tmp/xhs_explore_test.png"
        await browser.screenshot(explore_screenshot)
        print(f"📸 发现页截图: {explore_screenshot}")
        
        # 检查结果
        explore_content = await browser.page.content()
        if "登录" in explore_content and "手机号" in explore_content:
            print("\n⚠️ 检测到未登录状态 - Cookie 可能已过期或无效")
        else:
            print("\n✅ 看起来已登录成功！")
        
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(test_login_with_cookie())
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
