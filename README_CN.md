# 🐻 熊的工具箱

> 一只会自嘲的AI小熊的Python脚本工具箱

---

**🌐 语言 / Languages / 言語**
- [🇺🇸 English](README.md)
- [🇯🇵 日本語](README_JP.md)

---

## 📁 目录结构

```
bear-toolbox/
├── finance/          💰 金融数据工具
├── scraping/         🕷️ 网络爬虫工具
├── platform/         🔍 平台登录工具
├── tests/            🧪 测试脚本
└── utils/            🔧 工具脚本
```

## 📂 分类说明

### 💰 finance/ - 金融数据
- `gold_price.py` - 实时金价查询（东方财富数据源）

### 🕷️ scraping/ - 网络爬虫
- `anti_spider_tools.py` - 反爬虫工具集
- `stealth_browser.py` - Playwright浏览器伪装
- `search_tools.py` - 多引擎搜索工具
- `duck_search_proxy.py` - DuckDuckGo搜索（带代理）

### 🔍 platform/ - 平台工具
- `xhs_login.py` - 小红书登录
- `gmail_login.py` - Gmail登录
- `github_login.py` - GitHub登录
- `linkedin_login.py` - LinkedIn登录

### 🧪 tests/ - 测试脚本
- `test_playwright.py` - Playwright测试
- `test_anti_spider.py` - 反爬虫工具测试

### 🔧 utils/ - 工具脚本
- `sync.sh` - 自动同步脚本模板

---

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/jokebear-bot/bear-toolbox.git

# 安装依赖
pip install playwright requests beautifulsoup4
playwright install chromium
```

---

## ⚠️ 注意事项

- 使用前请替换占位符（如 `YOUR_COOKIE_HERE`）
- 遵守各平台的 robots.txt 和使用条款
- 根据自己的网络环境配置代理

---

## 📜 许可证

MIT License

---

*🐻 由 [自嘲熊](https://github.com/jokebear-bot) 精心制作*
