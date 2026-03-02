#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄金实时价格获取脚本 v4
数据源：Yahoo Finance (via yfinance)
安装：pip install yfinance
"""

import sys
from datetime import datetime

def get_gold_price():
    """获取黄金价格"""
    try:
        import yfinance as yf
        
        # GC=F 是 COMEX 黄金期货代码
        gold = yf.Ticker("GC=F")
        
        # 获取实时数据
        info = gold.info
        
        # 获取最近的价格数据
        hist = gold.history(period="1d")
        
        if not hist.empty:
            latest = hist.iloc[-1]
            return {
                "最新价": latest.get("Close"),
                "开盘": latest.get("Open"),
                "最高": latest.get("High"),
                "最低": latest.get("Low"),
                "昨收": info.get("previousClose"),
                " symbol": "GC=F (COMEX黄金期货)"
            }
    except ImportError:
        return {"错误": "请安装 yfinance: pip install yfinance"}
    except Exception as e:
        return {"错误": str(e)}
    
    return {}

def get_gld_etf():
    """获取黄金ETF(GLD)作为参考"""
    try:
        import yfinance as yf
        gld = yf.Ticker("GLD")
        info = gld.info
        return {
            "ETF价格": info.get("regularMarketPrice"),
            "昨收": info.get("regularMarketPreviousClose"),
            "symbol": "GLD (SPDR黄金ETF)"
        }
    except:
        return {}

if __name__ == "__main__":
    print("=" * 60)
    print(f"🪙 黄金实时行情 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 检查是否安装了yfinance
    try:
        import yfinance
    except ImportError:
        print("\n❌ 请先安装 yfinance 库：")
        print("   pip install yfinance")
        print("\n或运行：")
        print("   pip3 install yfinance")
        sys.exit(1)
    
    # 获取金价
    gold_data = get_gold_price()
    
    if "错误" in gold_data:
        print(f"\n❌ 获取失败: {gold_data['错误']}")
    elif gold_data:
        print("\n📊 COMEX黄金期货(GC=F)")
        price = gold_data.get("最新价")
        if price:
            print(f"   💰 最新: ${price:.2f}/盎司")
            
            # 计算人民币价格
            USD_CNY = 7.25
            OUNCE_TO_GRAM = 31.1035
            cny_per_gram = price * USD_CNY / OUNCE_TO_GRAM
            print(f"   💱 约 ¥{cny_per_gram:.2f}/克")
        
        if gold_data.get("最高"):
            print(f"   📈 最高: ${gold_data['最高']:.2f}")
        if gold_data.get("最低"):
            print(f"   📉 最低: ${gold_data['最低']:.2f}")
        if gold_data.get("昨收"):
            print(f"   📊 昨收: ${gold_data['昨收']:.2f}")
    
    # 黄金ETF参考
    gld = get_gld_etf()
    if gld and not gld.get("错误"):
        print(f"\n📊 黄金ETF(GLD)")
        print(f"   💰 价格: ${gld.get('ETF价格', '-')}")
    
    print("\n" + "=" * 60)
    print("💡 提示：")
    print("   • 数据来自 Yahoo Finance")
    print("   • 银行纸黄金价格通常在国际金价基础上加10-20元/克")
    print("   • 如需更精确报价，请查看银行App")
