#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄金实时价格获取脚本 v3
数据源：金投网 API
"""

import requests
import json
from datetime import datetime

def get_jintou_gold():
    """从金投网获取黄金价格"""
    try:
        # 金投网黄金价格API
        url = "https://api.jijinhao.com/quoteCenter/realTime.htm"
        params = {
            "code": "JO_92233",  # 国际黄金
            "_": str(int(datetime.now().timestamp() * 1000))
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://gold.cngold.org/"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_sina_forex_gold():
    """新浪外汇黄金"""
    try:
        url = "https://hq.sinajs.cn/list=fx_sxau"
        headers = {
            "Referer": "https://finance.sina.com.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'gbk'
        
        # 解析: var hq_str_fx_sxau="美元/盎司,2955.45,2945.30,0.00,0.34%,2958.20,2932.15,0.00,0.00,0.00,0.00,2025-02-25,08:59:52,0,0";
        data_str = response.text
        if 'var hq_str_' in data_str:
            parts = data_str.split('="')[1].rstrip('";').split(',')
            return {
                "名称": parts[0],
                "最新价": parts[1],
                "涨跌": parts[2],
                "涨跌幅": parts[4],
                "最高": parts[5],
                "最低": parts[6],
                "时间": f"{parts[12]} {parts[13]}"
            }
    except Exception as e:
        return {"error": str(e)}
    return {}

def get_boc_gold():
    """中国银行纸黄金参考（网页抓取）"""
    try:
        # 这是一个示例，实际可能需要更复杂的解析
        url = "https://www.boc.cn/sourcedb/whpj/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        # 实际解析需要HTML解析器，这里简化处理
        return {"info": "请访问 https://www.boc.cn/sourcedb/whpj/ 查看"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("=" * 60)
    print(f"🪙 黄金价格查询 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 新浪外汇黄金
    print("\n📊 新浪-国际黄金(XAU/USD)")
    sina = get_sina_forex_gold()
    if sina and "error" not in sina:
        print(f"   💰 最新: ${sina.get('最新价', '-')}/盎司")
        print(f"   📈 涨跌: {sina.get('涨跌', '-')} ({sina.get('涨跌幅', '-')})")
        print(f"   ⬆️ 最高: ${sina.get('最高', '-')}")
        print(f"   ⬇️ 最低: ${sina.get('最低', '-')}")
        print(f"   🕐 时间: {sina.get('时间', '-')}")
        
        # 计算人民币价格
        try:
            price = float(sina.get('最新价', 0))
            if price > 0:
                cny_per_gram = price * 7.25 / 31.1035
                print(f"   💱 约 ¥{cny_per_gram:.2f}/克 (按汇率7.25)")
        except:
            pass
    else:
        print(f"   获取失败: {sina.get('error', '未知错误')}")
    
    print("\n" + "=" * 60)
    print("💡 说明：")
    print("   • 以上数据来自新浪财经外汇频道")
    print("   • 银行纸黄金报价通常会有10-20元/克的溢价")
    print("   • 建议直接查看工行/建行手机App获取准确报价")
    print("   • 数据仅供参考，不构成投资建议")
