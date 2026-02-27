#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄金实时价格获取脚本
数据源：新浪财经实时行情API
"""

import requests
import json
import sys
from datetime import datetime

def get_sina_gold_price():
    """从新浪财经获取黄金实时价格"""
    # 新浪实时行情API
    # XAU为国际黄金现货，GC为COMEX黄金期货，AU为上海黄金
    symbols = {
        "国际黄金现货": "hf_XAU",
        "COMEX黄金": "hf_GC",
        "伦敦金": "hf_XAU",
        "上海黄金延期": "au0"
    }
    
    results = {}
    
    for name, symbol in symbols.items():
        try:
            if symbol.startswith("hf_"):
                # 外盘期货/现货
                url = f"https://hq.sinajs.cn/list={symbol}"
                headers = {
                    "Referer": "https://finance.sina.com.cn",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                response = requests.get(url, headers=headers, timeout=10)
                response.encoding = 'gbk'
                
                # 解析返回数据
                data_str = response.text
                if 'var hq_str_' in data_str:
                    # 提取数据部分
                    data = data_str.split('="')[1].rstrip('";').split(',')
                    if len(data) >= 8:
                        results[name] = {
                            "最新价": data[0],
                            "开盘价": data[1] if len(data) > 1 else "-",
                            "最高价": data[2] if len(data) > 2 else "-",
                            "最低价": data[3] if len(data) > 3 else "-",
                            "昨收": data[4] if len(data) > 4 else "-",
                            "时间": f"{data[-2]} {data[-1]}" if len(data) >= 2 else "-"
                        }
            else:
                # 内盘黄金
                url = f"https://hq.sinajs.cn/list=hf_{symbol}"
                headers = {
                    "Referer": "https://finance.sina.com.cn",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                response = requests.get(url, headers=headers, timeout=10)
                response.encoding = 'gbk'
                data_str = response.text
                if 'var hq_str_' in data_str:
                    data = data_str.split('="')[1].rstrip('";').split(',')
                    if len(data) >= 8:
                        results[name] = {
                            "最新价": data[0],
                            "开盘价": data[1] if len(data) > 1 else "-",
                            "最高价": data[2] if len(data) > 2 else "-",
                            "最低价": data[3] if len(data) > 3 else "-",
                            "昨收": data[4] if len(data) > 4 else "-",
                            "时间": f"{data[-2]} {data[-1]}" if len(data) >= 2 else "-"
                        }
        except Exception as e:
            results[name] = {"错误": str(e)}
    
    return results

def get_baidu_gold():
    """备用：百度股市通黄金数据"""
    try:
        url = "https://finance.pae.baidu.com/api/foreignquotation?srcid=5353&all=1&ktype=1&group=quotation_minute&query=现货黄金&code=XAU&market=gold&finClientType=pc"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        return data
    except Exception as e:
        return {"错误": str(e)}

def format_output(results):
    """格式化输出"""
    print("=" * 50)
    print(f"🪙 黄金实时行情 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 汇率（可根据实际情况调整）
    USD_CNY = 7.25
    OUNCE_TO_GRAM = 31.1035
    
    for name, data in results.items():
        print(f"\n📊 {name}")
        if "错误" in data:
            print(f"   获取失败: {data['错误']}")
        else:
            try:
                price_usd = float(data.get("最新价", 0))
                if price_usd > 1000:  # 可能是美元/盎司
                    price_cny_per_oz = price_usd * USD_CNY
                    price_cny_per_g = price_cny_per_oz / OUNCE_TO_GRAM
                    print(f"   💰 美元/盎司: ${price_usd:.2f}")
                    print(f"   💰 人民币/克: ¥{price_cny_per_g:.2f}")
                else:
                    print(f"   💰 价格: {price_usd}")
                
                if data.get("最高价") and data.get("最高价") != "-":
                    print(f"   📈 最高: {data['最高价']}")
                if data.get("最低价") and data.get("最低价") != "-":
                    print(f"   📉 最低: {data['最低价']}")
            except:
                for key, value in data.items():
                    print(f"   {key}: {value}")
    
    print("\n" + "=" * 50)
    print("💡 说明：人民币价格按汇率7.25估算，实际以银行报价为准")

if __name__ == "__main__":
    results = get_sina_gold_price()
    format_output(results)
    
    # 输出JSON格式供其他程序调用
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        print("\n[JSON输出]")
        print(json.dumps(results, ensure_ascii=False, indent=2))
