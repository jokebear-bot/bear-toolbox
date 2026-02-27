#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄金实时价格获取脚本 v6
数据源：东方财富 (最可靠)
"""

import requests
from datetime import datetime

def get_eastmoney_gold():
    """从东方财富获取黄金实时价格"""
    url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
    params = {
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fltt": "2",
        "invt": "2",
        "fields": "f2,f3,f4,f12,f13,f14,f18,f20,f21,f33,f34,f35,f36",
        "secids": "101.GC00Y,122.XAU,113.au0"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        data = response.json()
        
        results = {}
        if "data" in data and "diff" in data["data"]:
            for item in data["data"]["diff"]:
                code = item.get("f12")
                name = item.get("f14")
                price = item.get("f2")
                change = item.get("f4")
                change_pct = item.get("f3")
                prev_close = item.get("f18")
                high = item.get("f33")
                low = item.get("f34")
                
                results[code] = {
                    "名称": name,
                    "最新价": price,
                    "涨跌额": change,
                    "涨跌幅": change_pct,
                    "昨收": prev_close,
                    "最高": high,
                    "最低": low
                }
        return results
    except Exception as e:
        return {"错误": str(e)}

if __name__ == "__main__":
    print("=" * 65)
    print(f"🪙 黄金实时行情 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    
    # 汇率
    USD_CNY = 7.25
    OUNCE_TO_GRAM = 31.1035
    
    data = get_eastmoney_gold()
    
    if "错误" in data:
        print(f"\n❌ 获取失败: {data['错误']}")
    else:
        # COMEX黄金
        if "GC00Y" in data:
            print("\n📊 COMEX黄金期货 (GC00Y)")
            item = data["GC00Y"]
            price = item.get("最新价", 0)
            if price:
                cny_per_gram = price * USD_CNY / OUNCE_TO_GRAM
                print(f"   💰 美元/盎司: ${price:,.2f}")
                print(f"   💱 约人民币/克: ¥{cny_per_gram:,.2f}")
                
                change = item.get("涨跌额", 0)
                change_pct = item.get("涨跌幅", 0)
                if change and change > 0:
                    print(f"   📈 涨跌: +{change:,.2f} (+{change_pct}%)")
                elif change and change < 0:
                    print(f"   📉 涨跌: {change:,.2f} ({change_pct}%)")
                
                if item.get("最高"):
                    print(f"   ⬆️ 最高: ${item['最高']:,.2f}")
                if item.get("最低"):
                    print(f"   ⬇️ 最低: ${item['最低']:,.2f}")
                if item.get("昨收"):
                    print(f"   📊 昨收: ${item['昨收']:,.2f}")
        
        # 伦敦金/美元
        if "XAU" in data:
            print("\n📊 伦敦金现货 (XAU/USD)")
            item = data["XAU"]
            price = item.get("最新价", 0)
            if price:
                cny_per_gram = price * USD_CNY / OUNCE_TO_GRAM
                print(f"   💰 美元/盎司: ${price:,.2f}")
                print(f"   💱 约人民币/克: ¥{cny_per_gram:,.2f}")
        
        # 沪金
        if "au0" in data:
            print("\n📊 沪金主连 (au0)")
            item = data["au0"]
            price = item.get("最新价", 0)
            if price:
                print(f"   💰 人民币/克: ¥{price:,.2f}")
    
    print("\n" + "=" * 65)
    print("💡 说明：")
    print("   • 数据来源: 东方财富")
    print("   • 银行纸黄金通常在国际金价基础上加10-20元/克溢价")
    print("   • 人民币价格按汇率7.25估算")
    print("   • 本数据仅供参考，不构成投资建议")
