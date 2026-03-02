#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📧 Gmail IMAP 邮件读取
直接读取收件箱邮件
"""

import imaplib
import email
from email.header import decode_header
from datetime import datetime

def read_gmail():
    EMAIL = "your_email@gmail.com"
    PASSWORD = "YOUR_PASSWORD_HERE"
    
    try:
        # 连接 Gmail IMAP
        print("📧 连接 Gmail IMAP...")
        imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        
        # 登录
        print("🔑 登录中...")
        imap.login(EMAIL, PASSWORD)
        print("✅ 登录成功！\n")
        
        # 选择收件箱
        imap.select("INBOX")
        
        # 搜索未读邮件
        print("🔍 搜索邮件...")
        status, messages = imap.search(None, "ALL")  # 读取所有邮件
        
        if status != "OK":
            print("❌ 无法搜索邮件")
            return
        
        message_ids = messages[0].split()
        print(f"📨 找到 {len(message_ids)} 封邮件\n")
        
        # 读取最新的5封邮件
        for i, msg_id in enumerate(reversed(message_ids[-5:]), 1):
            print(f"{'='*60}")
            print(f"📧 邮件 #{i}")
            print(f"{'='*60}")
            
            status, msg_data = imap.fetch(msg_id, "(RFC822)")
            
            if status != "OK":
                continue
            
            raw_email = msg_data[0][1]
            email_message = email.message_from_bytes(raw_email)
            
            # 获取发件人
            from_header = email_message.get("From", "Unknown")
            print(f"📤 发件人: {from_header}")
            
            # 获取主题
            subject = email_message.get("Subject", "No Subject")
            if subject:
                subject_decoded = decode_header(subject)
                subject_str = ""
                for part, charset in subject_decoded:
                    if isinstance(part, bytes):
                        subject_str += part.decode(charset or 'utf-8', errors='ignore')
                    else:
                        subject_str += part
                subject = subject_str
            print(f"📋 主题: {subject}")
            
            # 获取日期
            date = email_message.get("Date", "Unknown")
            print(f"📅 日期: {date}")
            
            # 获取内容
            print(f"\n📝 内容:")
            print("-" * 60)
            
            def get_email_body(msg):
                """获取邮件正文"""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition", ""))
                        
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            try:
                                body = part.get_payload(decode=True)
                                charset = part.get_content_charset() or 'utf-8'
                                return body.decode(charset, errors='ignore')
                            except:
                                continue
                        elif content_type == "text/html" and "attachment" not in content_disposition:
                            try:
                                body = part.get_payload(decode=True)
                                charset = part.get_content_charset() or 'utf-8'
                                return body.decode(charset, errors='ignore')
                            except:
                                continue
                else:
                    try:
                        body = msg.get_payload(decode=True)
                        charset = msg.get_content_charset() or 'utf-8'
                        return body.decode(charset, errors='ignore')
                    except:
                        return "无法解码内容"
                return "无内容"
            
            body = get_email_body(email_message)
            # 只显示前500字符
            if len(body) > 500:
                print(body[:500] + "...")
            else:
                print(body)
            
            print()
        
        # 关闭连接
        imap.close()
        imap.logout()
        print("✅ 完成")
        
    except imaplib.IMAP4.error as e:
        print(f"❌ IMAP 错误: {e}")
        if "AUTHENTICATIONFAILED" in str(e):
            print("💡 可能需要：")
            print("   1. 开启 Gmail 的 IMAP 访问: 设置 -> 转发和 POP/IMAP -> IMAP 访问")
            print("   2. 使用应用专用密码（如果开了两步验证）")
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    read_gmail()
