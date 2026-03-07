#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎭 Playwright 高级反爬方案
使用真实浏览器绕过复杂的反爬机制

安装依赖:
    pip install playwright
    playwright install chromium
"""

import asyncio
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from typing import Optional, Dict, Any
import json
import random

class StealthBrowser:
    """
    隐形浏览器 - 高级反爬方案
    
    绕过技术：
    - WebDriver 检测
    - Canvas 指纹
    - WebGL 指纹  
    - 插件检测
    - 屏幕尺寸检测
    - 自动化特征移除
    """
    
    def __init__(self, use_proxy: bool = True, headless: bool = False):
        self.use_proxy = use_proxy
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    async def __aenter__(self):
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def start(self):
        """启动隐形浏览器"""
        self.playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = [
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--disable-gpu',
            '--window-size=1920,1080',
        ]
        
        # 启动浏览器
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=browser_args
        )
        
        # 创建上下文（带指纹伪装）
        context_options = {
            "viewport": {"width": 1920, "height": 1080},
            "user_agent": self._get_random_ua(),
            "locale": "zh-CN",
            "timezone_id": "Asia/Shanghai",
            "permissions": ["geolocation"],
            "color_scheme": "light",
        }
        
        # 添加代理（系统已配置）
        if self.use_proxy:
            # 检查代理是否可用
            try:
                import requests
                requests.get("https://www.google.com/robots.txt", 
                           proxies={"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"},
                           timeout=5)
                context_options["proxy"] = {"server": "http://127.0.0.1:7890"}
            except:
                print("⚠️ 代理不可用，使用直连模式")
        
        self.context = await self.browser.new_context(**context_options)
        
        # 添加 stealth 脚本
        await self._apply_stealth_scripts()
        
        # 创建页面
        self.page = await self.context.new_page()
        
        return self
    
    async def _apply_stealth_scripts(self):
        """应用隐形脚本 - 移除自动化特征"""
        
        stealth_scripts = [
            # 1. 移除 webdriver 标志
            """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            """,
            
            # 2. 伪装 chrome
            """
            window.chrome = {
                runtime: {},
                loadTimes: function() {},
                csi: function() {},
                app: {}
            };
            """,
            
            # 3. 伪装 plugins
            """
            Object.defineProperty(navigator, 'plugins', {
                get: () => [
                    {
                        0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"},
                        description: "Portable Document Format",
                        filename: "internal-pdf-viewer",
                        length: 1,
                        name: "Chrome PDF Plugin"
                    },
                    {
                        0: {type: "application/pdf", suffixes: "pdf", description: ""},
                        description: "Portable Document Format",
                        filename: "internal-pdf-viewer2",
                        length: 1,
                        name: "Chrome PDF Viewer"
                    }
                ]
            });
            """,
            
            # 4. 伪装 languages
            """
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en-US', 'en']
            });
            """,
            
            # 5. 移除 automation 特征
            """
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            """,
            
            # 6. 伪装 notification permission
            """
            const originalNotification = window.Notification;
            Object.defineProperty(window, 'Notification', {
                get: function() {
                    return originalNotification;
                },
                set: function(value) {
                    originalNotification = value;
                }
            });
            Object.defineProperty(Notification, 'permission', {
                get: function() {
                    return 'default';
                }
            });
            """,
            
            # 7. 防止 iframe 检测
            """
            window.addEventListener('load', function() {
                const iframes = document.getElementsByTagName('iframe');
                for (let i = 0; i < iframes.length; i++) {
                    try {
                        const iframe = iframes[i];
                        iframe.contentWindow.navigator.webdriver = undefined;
                    } catch (e) {}
                }
            });
            """,
            
            # 8. 伪装 webgl
            """
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return 'Intel Inc.';
                }
                if (parameter === 37446) {
                    return 'Intel Iris OpenGL Engine';
                }
                return getParameter(parameter);
            };
            """,
        ]
        
        # 在所有页面应用脚本
        await self.context.add_init_script("\n".join(stealth_scripts))
    
    def _get_random_ua(self) -> str:
        """获取随机 User-Agent"""
        uas = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        ]
        return random.choice(uas)
    
    async def goto(self, url: str, wait_for: str = None, timeout: int = 30000):
        """
        访问页面
        
        Args:
            url: 目标 URL
            wait_for: 等待的元素选择器（如 "article" 或 "networkidle"）
            timeout: 超时时间（毫秒）
        """
        if not self.page:
            raise RuntimeError("Browser not started")
        
        # 随机延迟（模拟人类）
        await asyncio.sleep(random.uniform(0.5, 2))
        
        response = await self.page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        
        # 额外等待
        if wait_for:
            try:
                await self.page.wait_for_selector(wait_for, timeout=timeout)
            except:
                pass
        else:
            # 等待网络空闲
            await asyncio.sleep(2)
        
        return response
    
    async def get_content(self) -> str:
        """获取页面内容"""
        if not self.page:
            raise RuntimeError("Browser not started")
        return await self.page.content()
    
    async def get_text(self, selector: str) -> str:
        """获取元素文本"""
        try:
            element = await self.page.query_selector(selector)
            if element:
                return await element.inner_text()
        except:
            pass
        return ""
    
    async def scroll_to_bottom(self):
        """滚动到页面底部（模拟人类）"""
        await self.page.evaluate("""
            async () => {
                await new Promise((resolve) => {
                    let totalHeight = 0;
                    const distance = 100 + Math.random() * 100;
                    const timer = setInterval(() => {
                        const scrollHeight = document.body.scrollHeight;
                        window.scrollBy(0, distance);
                        totalHeight += distance;
                        
                        if (totalHeight >= scrollHeight) {
                            clearInterval(timer);
                            resolve();
                        }
                    }, 100 + Math.random() * 200);
                });
            }
        """)
    
    async def screenshot(self, path: str = None):
        """截图"""
        if path:
            return await self.page.screenshot(path=path, full_page=True)
        return await self.page.screenshot()
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()


# ============ 特定网站爬取器 ============

class XiaohongshuCrawler:
    """小红书爬取器（使用真实浏览器）"""
    
    def __init__(self, stealth_browser: StealthBrowser = None):
        self.browser = stealth_browser
        self.external_browser = stealth_browser is not None
    
    async def get_note(self, note_url: str) -> Optional[Dict[str, Any]]:
        """获取笔记内容"""
        own_browser = False
        
        try:
            if not self.browser:
                self.browser = StealthBrowser(headless=True)
                await self.browser.start()
                own_browser = True
            
            await self.browser.goto(note_url, wait_for="img")
            
            # 模拟人类滚动
            await self.browser.scroll_to_bottom()
            await asyncio.sleep(1)
            
            # 提取内容
            content = await self.browser.page.evaluate("""
                () => {
                    const title = document.querySelector('h1')?.innerText || '';
                    const desc = document.querySelector('.desc')?.innerText || 
                                 document.querySelector('[class*="content"]')?.innerText || '';
                    const author = document.querySelector('.author-name')?.innerText || 
                                   document.querySelector('[class*="nickname"]')?.innerText || '';
                    
                    const images = Array.from(document.querySelectorAll('img'))
                        .map(img => img.src)
                        .filter(src => src && src.includes('xiaohongshu'));
                    
                    return { title, desc, author, images };
                }
            """)
            
            return content
            
        except Exception as e:
            print(f"❌ 小红书爬取失败: {e}")
            return None
            
        finally:
            if own_browser:
                await self.browser.close()
    
    async def search(self, keyword: str, max_results: int = 10) -> list:
        """搜索笔记"""
        search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}"
        
        try:
            if not self.browser:
                self.browser = StealthBrowser(headless=True)
                await self.browser.start()
            
            await self.browser.goto(search_url, wait_for="article")
            await asyncio.sleep(3)  # 等待内容加载
            
            # 提取搜索结果
            results = await self.browser.page.evaluate(f"""
                () => {{
                    const cards = document.querySelectorAll('article, [class*="card"]');
                    const data = [];
                    for (let i = 0; i < Math.min({max_results}, cards.length); i++) {{
                        const card = cards[i];
                        const link = card.querySelector('a')?.href || '';
                        const title = card.querySelector('h3, h2, .title')?.innerText || '';
                        const cover = card.querySelector('img')?.src || '';
                        if (link) {{
                            data.push({{ link, title, cover }});
                        }}
                    }}
                    return data;
                }}
            """)
            
            return results
            
        except Exception as e:
            print(f"❌ 小红书搜索失败: {e}")
            return []


class FTCrawler:
    """Financial Times 爬取器"""
    
    def __init__(self, stealth_browser: StealthBrowser = None):
        self.browser = stealth_browser
    
    async def get_article(self, url: str) -> Optional[Dict[str, str]]:
        """获取 FT 文章内容"""
        own_browser = False
        
        try:
            if not self.browser:
                self.browser = StealthBrowser(headless=True)
                await self.browser.start()
                own_browser = True
            
            await self.browser.goto(url, wait_for="article")
            await asyncio.sleep(2)
            
            # 提取文章内容
            content = await self.browser.page.evaluate("""
                () => {
                    const title = document.querySelector('h1')?.innerText || 
                                  document.querySelector('.article-headline')?.innerText || '';
                    
                    const summary = document.querySelector('.article-standfirst')?.innerText || '';
                    
                    const paragraphs = Array.from(document.querySelectorAll('.article-body p, article p'))
                        .map(p => p.innerText)
                        .filter(text => text.length > 20)
                        .slice(0, 10);
                    
                    const author = document.querySelector('.article-author')?.innerText || '';
                    const date = document.querySelector('time')?.innerText || '';
                    
                    return { title, summary, paragraphs, author, date };
                }
            """)
            
            return content
            
        except Exception as e:
            print(f"❌ FT 爬取失败: {e}")
            return None
            
        finally:
            if own_browser:
                await self.browser.close()


# ============ 演示 ============

async def demo():
    """演示高级反爬"""
    print("🎭 Playwright 高级反爬演示\n")
    
    # 示例：访问 httpbin 测试伪装效果
    async with StealthBrowser(headless=True) as browser:
        print("🔍 测试浏览器伪装...")
        await browser.goto("https://httpbin.org/headers")
        
        # 获取请求头信息
        content = await browser.page.content()
        print("\n📊 浏览器发送的请求头:")
        
        # 提取 headers 部分
        import re
        headers_match = re.search(r'<pre>({.*?})</pre>', content, re.DOTALL)
        if headers_match:
            import json
            headers = json.loads(headers_match.group(1))
            for key, value in headers.get("headers", {}).items():
                print(f"  {key}: {value}")
        
        # 测试 WebDriver 检测
        print("\n🔍 测试 WebDriver 检测绕过...")
        await browser.goto("https://bot.sannysoft.com/")
        await asyncio.sleep(2)
        
        # 截图保存
        await browser.screenshot("/tmp/bot_test.png")
        print("  📸 已保存截图到 /tmp/bot_test.png")
        
        # 检查结果
        result = await browser.page.evaluate("""
            () => {
                const webdriver = navigator.webdriver;
                const plugins = navigator.plugins.length;
                const languages = navigator.languages;
                return { webdriver, plugins, languages };
            }
        """)
        
        print(f"\n🧪 检测指标:")
        print(f"  navigator.webdriver: {result['webdriver']} (应为 undefined/null)")
        print(f"  navigator.plugins: {result['plugins']} 个 (应 > 0)")
        print(f"  navigator.languages: {result['languages']}")
    
    print("\n✅ 演示完成")


if __name__ == "__main__":
    asyncio.run(demo())
