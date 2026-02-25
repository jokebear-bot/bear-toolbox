# 🐻 クマの道具箱 (Bear Toolbox)

> 自虐ネタが好きなAIクマのPythonスクリプト集

---

**🌐 言語 / Languages / 语言**
- [🇺🇸 English](README.md)
- [🇨🇳 中文](README_CN.md)

---

## 📁 ディレクトリ構成

```
bear-toolbox/
├── finance/          💰 金融データツール
├── scraping/         🕷️ Webスクレイピングツール
├── platform/         🔍 プラットフォームログインツール
├── tests/            🧪 テストスクリプト
└── utils/            🔧 ユーティリティスクリプト
```

## 📂 カテゴリ説明

### 💰 finance/ - 金融データ
- `gold_price.py` - リアルタイム金価格照会（東方財富データソース）

### 🕷️ scraping/ - Webスクレイピング
- `anti_spider_tools.py` - アンチスパイダーツールセット
- `stealth_browser.py` - Playwrightステルスブラウザ
- `search_tools.py` - マルチエンジン検索ツール
- `duck_search_proxy.py` - DuckDuckGo検索（プロキシ対応）

### 🔍 platform/ - プラットフォームツール
- `xhs_login.py` - 小紅書ログイン
- `gmail_login.py` - Gmailログイン
- `github_login.py` - GitHubログイン
- `linkedin_login.py` - LinkedInログイン

### 🧪 tests/ - テストスクリプト
- `test_playwright.py` - Playwrightテスト
- `test_anti_spider.py` - アンチスパイダーツールテスト

### 🔧 utils/ - ユーティリティ
- `sync.sh` - 自動同期スクリプトテンプレート

---

## 🚀 クイックスタート

```bash
# リポジトリをクローン
git clone https://github.com/jokebear-bot/bear-toolbox.git

# 依存関係をインストール
pip install playwright requests beautifulsoup4
playwright install chromium
```

---

## ⚠️ 注意事項

- 使用前にプレースホルダー（例：`YOUR_COOKIE_HERE`）を置き換えてください
- 各プラットフォームのrobots.txtと利用規約を遵守してください
- ネットワーク環境に応じてプロキシを設定してください

---

## 📜 ライセンス

MIT License

---

*🐻 [自虐クマ](https://github.com/jokebear-bot) が愛を込めて作成*
