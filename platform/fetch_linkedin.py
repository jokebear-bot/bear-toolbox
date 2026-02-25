#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 LinkedIn 简历抓取
使用 Playwright 访问用户领英页面
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stealth_browser import StealthBrowser

async def fetch_linkedin():
    """抓取领英简历"""
    print("=" * 60)
    print("🔗 抓取 LinkedIn 简历")
    print("=" * 60)
    
    async with StealthBrowser(headless=True) as browser:
        print("\n🚀 正在打开 LinkedIn...")
        
        # 访问用户领英页面
        await browser.goto("https://www.your-linkedin-profile", wait_for="body")
        await asyncio.sleep(3)
        
        print("✅ 页面已加载")
        
        # 截图
        screenshot = "/tmp/linkedin_profile.png"
        await browser.screenshot(screenshot)
        print(f"📸 已保存截图: {screenshot}")
        
        # 尝试提取信息
        profile_info = await browser.page.evaluate("""
            () => {
                const data = {
                    name: '',
                    headline: '',
                    about: '',
                    experience: [],
                    education: []
                };
                
                // 姓名
                const nameEl = document.querySelector('h1');
                if (nameEl) data.name = nameEl.innerText.trim();
                
                // 头衔
                const headlineEl = document.querySelector('[class*="headline"], .pv-top-card__headline');
                if (headlineEl) data.headline = headlineEl.innerText.trim();
                
                // About
                const aboutEl = document.querySelector('[class*="about"] [class*="summary"], [class*="inline-show-more-text"]');
                if (aboutEl) data.about = aboutEl.innerText.trim();
                
                // 工作经历
                const expItems = document.querySelectorAll('[class*="experience"], .pv-experience-section__summary-item');
                expItems.forEach(item => {
                    const title = item.querySelector('h3, [class*="title"]')?.innerText?.trim();
                    const company = item.querySelector('[class*="company"], p')?.innerText?.trim();
                    if (title || company) {
                        data.experience.push({ title, company });
                    }
                });
                
                // 教育
                const eduItems = document.querySelectorAll('[class*="education"]');
                eduItems.forEach(item => {
                    const school = item.querySelector('h3, [class*="school"]')?.innerText?.trim();
                    const degree = item.querySelector('[class*="degree"]')?.innerText?.trim();
                    if (school) {
                        data.education.push({ school, degree });
                    }
                });
                
                return data;
            }
        """)
        
        print("\n📄 提取的信息:")
        print(f"姓名: {profile_info.get('name', 'N/A')}")
        print(f"头衔: {profile_info.get('headline', 'N/A')}")
        
        if profile_info.get('about'):
            print(f"\n关于:\n{profile_info['about'][:300]}...")
        
        if profile_info.get('experience'):
            print(f"\n工作经历 ({len(profile_info['experience'])} 条):")
            for exp in profile_info['experience'][:3]:
                print(f"  - {exp.get('title', '')} @ {exp.get('company', '')}")
        
        # 保存完整内容
        content = await browser.get_content()
        with open('/tmp/linkedin_content.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n📄 完整 HTML 已保存到 /tmp/linkedin_content.html")
        
    print("\n" + "=" * 60)
    print("✅ 完成")
    print("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(fetch_linkedin())
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
