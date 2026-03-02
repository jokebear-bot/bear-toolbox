#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄金实时价格获取脚本 v2
数据源：东方财富
"""

import requests
import json
from datetime import datetime

def get_eastmoney_gold():
    """从东方财富获取黄金期货价格"""
    # 东方财富API - COMEX黄金
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fltt": "2",
        "invt": "2",
        "fields": "f43,f44,f45,f46,f47,f48,f57,f58,f60",
        "secid": "101.GC00Y"  # COMEX黄金主力
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if data.get("data"):
            d = data["data"]
            return {
                "最新价": d.get("f43"),
                "今开": d.get("f44"),
                "最高": d.get("f45"),
                "最低": d.get("f46"),
                "昨收": d.get("f60"),
                "名称": d.get("f58"),
                "代码": d.get("f57")
            }
    except Exception as e:
        return {"错误": str(e)}
    
    return {}

def get_london_gold():
    """获取伦敦金现货"""
    # 尝试使用外汇黄金的接口
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fltt": "2",
        "invt": "2", 
        "fields": "f43,f44,f45,f46,f47,f48,f57,f58,f60",
        "secid": "122.XAU"  # 伦敦金
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if data.get("data"):
            d = data["data"]
            return {
                "最新价": d.get("f43"),
                "今开": d.get("f44"),
                "最高": d.get("f45"),
                "最低": d.get("f46"),
                "昨收": d.get("f60"),
                "名称": d.get("f58"),
                "代码": d.get("f57")
            }
    except Exception as e:
        return {"错误": str(e)}
    
    return {}

def get_sh_gold():
    """获取上海黄金"""
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fltt": "2",
        "invt": "2",
        "fields": "f43,f44,f45,f46,f47,f48,f57,f58,f60",
        "secid": "113.au0"  # 沪金主力
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if data.get("data"):
            d = data["data"]
            return {
                "最新价": d.get("f43"),
                "今开": d.get("f44"),
                "最高": d.get("f45"),
                "最低": d.get("f46"),
                "昨收": d.get("f60"),
                "名称": d.get("f58"),
                "代码": d.get("f57")
            }
    except Exception as e:
        return {"错误": str(e)}
    
    return {}

def format_price(value):
    """格式化价格"""
    if value is None:
        return "-"
    try:
        return f"{float(value):.2f}"
    except:
        return str(value)

if __name__ == "__main__":
    print("=" * 60)
    print(f"🪙 黄金实时行情 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 汇率
    USD_CNY = 7.25
    OUNCE_TO_GRAM = 31.1035
    
    # COMEX黄金
    print("\n📊 COMEX黄金期货")
    comex = get_eastmoney_gold()
    if comex:
        if "错误" in comex:
            print(f"   获取失败: {comex['错误']}")
        else:
            price = comex.get("最新价")
            if price:
                price_usd = float(price)
                price_cny_g = price_usd * USD_CNY / OUNCE_TO_GRAM
                print(f"   💰 美元/盎司: ${format_price(price)}")
                print(f"   💰 约人民币/克: ¥{price_cny_g:.2f}")
                print(f"   📈 最高: ${format_price(comex.get('最高'))}")
                print(f"   📉 最低: ${format_price(comex.get('最低'))}")
                print(f"   📊 昨收: ${format_price(comex.get('昨收'))}")
    
    # 伦敦金
    print("\n📊 伦敦金现货")
    london = get_london_gold()
    if london and not london.get("错误"):
        price = london.get("最新价")
        if price:
            try:
                price_usd = float(price)
                price_cny_g = price_usd * USD_CNY / OUNCE_TO_GRAM
                print(f"   💰 美元/盎司: ${format_price(price)}")
                print(f"   💰 约人民币/克: ¥{price_cny_g:.2f}")
            except:
                print(f"   💰 价格: {price}")
    else:
        print("   暂无法获取")
    
    # 沪金
    print("\n📊 上海黄金(沪金主连)")
    sh = get_sh_gold()
    if sh:
        if "错误" in sh:
            print(f"   获取失败: {sh['错误']}")
        else:
            price = sh.get("最新价")
            if price:
                print(f"   💰 人民币/克: ¥{format_price(price)}")
                print(f"   📈 最高: ¥{format_price(sh.get('最高'))}")
                print(f"   📉 最低: ¥{format_price(sh.get('最低'))}")
    
    print("\n" + "=" * 60)
    print("💡 提示：")
    print("   • 国际金价按汇率7.25估算，实际以银行报价为准")
    print("   • 银行纸黄金通常在国际金价基础上加10-20元/克")
    print("   • 本脚本数据仅供参考，不构成投资建议")
