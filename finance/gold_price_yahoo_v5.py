#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄金实时价格获取脚本 v5
数据源：Yahoo Finance (无需安装 yfinance，直接调用API)
"""

import requests
import json
import re
from datetime import datetime

def get_yahoo_gold_price():
    """直接从Yahoo Finance获取黄金价格"""
    # GC=F 是 COMEX 黄金期货代码
    symbol = "GC=F"
    
    # Yahoo Finance 的图表API
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    
    params = {
        "interval": "1d",
        "range": "1d"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        data = response.json()
        
        if "chart" in data and "result" in data["chart"] and data["chart"]["result"]:
            result = data["chart"]["result"][0]
            meta = result.get("meta", {})
            
            # 获取最新价格
            regular_market_price = meta.get("regularMarketPrice")
            previous_close = meta.get("previousClose")
            
            return {
                "最新价": regular_market_price,
                "昨收": previous_close,
                "货币": meta.get("currency"),
                "symbol": symbol,
                "交易所": meta.get("exchangeName")
            }
        else:
            return {"错误": "无法获取数据"}
            
    except Exception as e:
        return {"错误": str(e)}

def get_gld_etf():
    """获取黄金ETF(GLD)作为参考"""
    symbol = "GLD"
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    params = {"interval": "1d", "range": "1d"}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        data = response.json()
        
        if "chart" in data and "result" in data["chart"] and data["chart"]["result"]:
            result = data["chart"]["result"][0]
            meta = result.get("meta", {})
            return {
                "最新价": meta.get("regularMarketPrice"),
                "昨收": meta.get("previousClose"),
                "symbol": "GLD"
            }
    except Exception as e:
        return {"错误": str(e)}
    return {}

def get_silver_price():
    """获取白银价格作为参考"""
    symbol = "SI=F"
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    params = {"interval": "1d", "range": "1d"}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        data = response.json()
        
        if "chart" in data and "result" in data["chart"] and data["chart"]["result"]:
            result = data["chart"]["result"][0]
            meta = result.get("meta", {})
            return {
                "最新价": meta.get("regularMarketPrice"),
                "symbol": "SI=F (白银期货)"
            }
    except:
        pass
    return {}

if __name__ == "__main__":
    print("=" * 65)
    print(f"🪙 黄金实时行情 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    
    # 汇率
    USD_CNY = 7.25
    OUNCE_TO_GRAM = 31.1035
    
    # COMEX黄金
    print("\n📊 COMEX黄金期货 (GC=F)")
    gold = get_yahoo_gold_price()
    
    if "错误" in gold:
        print(f"   ❌ 获取失败: {gold['错误']}")
    elif gold.get("最新价"):
        price = gold["最新价"]
        prev = gold.get("昨收", price)
        change = price - prev if prev else 0
        change_pct = (change / prev * 100) if prev else 0
        
        # 计算人民币价格
        cny_per_gram = price * USD_CNY / OUNCE_TO_GRAM
        
        print(f"   💰 美元/盎司: ${price:,.2f}")
        print(f"   💱 约人民币/克: ¥{cny_per_gram:,.2f}")
        
        if change >= 0:
            print(f"   📈 涨跌: +${change:.2f} (+{change_pct:.2f}%)")
        else:
            print(f"   📉 涨跌: ${change:.2f} ({change_pct:.2f}%)")
        
        if gold.get("昨收"):
            print(f"   📊 昨收: ${prev:,.2f}")
    
    # 黄金ETF
    gld = get_gld_etf()
    if gld and not gld.get("错误") and gld.get("最新价"):
        print(f"\n📊 SPDR黄金ETF (GLD)")
        print(f"   💰 价格: ${gld['最新价']:.2f}")
    
    # 白银
    silver = get_silver_price()
    if silver and silver.get("最新价"):
        print(f"\n📊 COMEX白银期货 (SI=F)")
        print(f"   💰 价格: ${silver['最新价']:.2f}/盎司")
    
    print("\n" + "=" * 65)
    print("💡 说明：")
    print("   • 数据来源: Yahoo Finance")
    print("   • 银行纸黄金通常在国际金价基础上加10-20元/克溢价")
    print("   • 人民币价格按汇率7.25估算")
    print("   • 本数据仅供参考，不构成投资建议")
