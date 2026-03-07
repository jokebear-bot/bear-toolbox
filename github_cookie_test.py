#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐙 GitHub Cookie 登录测试
使用用户提供的 Cookie 访问 GitHub
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stealth_browser import StealthBrowser

# 用户提供的 Cookie
USER_COOKIE = "YOUR_COOKIE_HERE"

async def github_cookie_login():
    """使用 Cookie 登录 GitHub"""
    print("=" * 60)
    print("🐙 GitHub Cookie 登录测试")
    print("=" * 60)
    
    async with StealthBrowser(headless=True) as browser:
        print("\n🚀 正在打开 GitHub...")
        
        # 先访问 GitHub
        await browser.goto("https://github.com", wait_for="body")
        print("✅ GitHub 已加载")
        
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
                    'domain': '.github.com',
                    'path': '/'
                })
        
        await browser.context.add_cookies(cookies)
        print(f"✅ 已设置 {len(cookies)} 个 Cookie")
        
        # 刷新页面
        print("\n🔄 刷新页面...")
        await browser.page.reload()
        await asyncio.sleep(3)
        
        # 检查登录状态
        print("\n🔍 检查登录状态...")
        
        # 查找用户名元素
        user_info = await browser.page.evaluate("""
            () => {
                // 查找头像
                const avatar = document.querySelector('[data-testid="global-profile-menu"] img, .avatar-user img, [class*="avatar"] img');
                // 查找用户名链接
                const usernameLink = document.querySelector('[data-testid="global-profile-menu"], [aria-label*="profile"]');
                // 检查是否有登录/注册按钮
                const signupBtn = document.querySelector('a[href*="signup"]');
                const signinBtn = document.querySelector('a[href*="login"]');
                const headerSignin = document.querySelector('a[href="/login"]');
                
                return {
                    hasAvatar: !!avatar,
                    avatarSrc: avatar?.src || '',
                    hasUsernameLink: !!usernameLink,
                    hasSignupBtn: !!signupBtn,
                    hasSigninBtn: !!(signinBtn || headerSignin),
                    url: window.location.href,
                    title: document.title
                };
            }
        """)
        
        print(f"\n📊 页面信息:")
        print(f"   URL: {user_info['url']}")
        print(f"   标题: {user_info['title']}")
        print(f"   检测到头像: {'✅' if user_info['hasAvatar'] else '❌'}")
        if user_info['avatarSrc']:
            print(f"   头像地址: {user_info['avatarSrc'][:50]}...")
        print(f"   登录按钮: {'❌ 未检测到' if not user_info['hasSigninBtn'] else '⚠️ 检测到'}")
        print(f"   注册按钮: {'❌ 未检测到' if not user_info['hasSignupBtn'] else '⚠️ 检测到'}")
        
        # 如果看起来已登录，尝试获取更多信息
        if user_info['hasAvatar'] and not user_info['hasSigninBtn']:
            print("\n✅ 看起来已登录！")
            
            # 访问 profile 页面
            print("\n🌐 访问 Profile 页面...")
            await browser.goto("https://github.com/settings/profile", wait_for="body")
            await asyncio.sleep(2)
            
            profile_info = await browser.page.evaluate("""
                () => {
                    const nameEl = document.querySelector('[name="user[profile_name]"]');
                    const bioEl = document.querySelector('[name="user[profile_bio]"]');
                    const loginEl = document.querySelector('[name="user[login]"]') || 
                                   document.querySelector('.user-profile-name');
                    
                    return {
                        name: nameEl?.value || '',
                        bio: bioEl?.value || '',
                        login: loginEl?.value || loginEl?.innerText || '',
                        url: window.location.href
                    };
                }
            """)
            
            print(f"\n👤 用户信息:")
            print(f"   登录名: {profile_info['login']}")
            if profile_info['name']:
                print(f"   显示名: {profile_info['name']}")
            if profile_info['bio']:
                print(f"   Bio: {profile_info['bio'][:50]}")
        else:
            print("\n⚠️ 似乎未登录，Cookie 可能不完整或已过期")
        
        # 截图
        screenshot = "/tmp/github_cookie_test.png"
        await browser.screenshot(screenshot)
        print(f"\n📸 已保存截图: {screenshot}")
        
    print("\n" + "=" * 60)
    print("✅ 完成")
    print("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(github_cookie_login())
    except KeyboardInterrupt:
        print("\n👋 已退出")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
