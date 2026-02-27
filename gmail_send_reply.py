#!/usr/bin/env python3
"""
Gmail 回复发送脚本
- 读取待回复邮件列表
- 根据用户确认发送回复
"""

import json
import os
import base64
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

PENDING_FILE = '/tmp/gmail_pending_replies.json'

def get_gmail_service():
    """获取 Gmail API 服务对象"""
    creds = None
    token_path = '/root/.openclaw/workspace/config/gmail_token.pickle'
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("Gmail 未登录")
    
    return build('gmail', 'v1', credentials=creds)


def load_pending_replies():
    """加载待回复邮件列表"""
    if not os.path.exists(PENDING_FILE):
        return None
    
    with open(PENDING_FILE, 'r') as f:
        return json.load(f)


def send_reply(email_index, custom_message=None):
    """
    发送回复邮件
    
    Args:
        email_index: 邮件编号（从1开始）
        custom_message: 自定义回复内容（可选，覆盖默认草稿）
    """
    try:
        # 加载待回复列表
        pending = load_pending_replies()
        if not pending:
            return "❌ 没有待回复的邮件列表，请先运行邮件检查"
        
        emails = pending.get('emails', [])
        if not emails:
            return "❌ 待回复列表为空"
        
        # 检查索引
        if email_index < 1 or email_index > len(emails):
            return f"❌ 无效的邮件编号 {email_index}，当前共有 {len(emails)} 封待回复邮件"
        
        email = emails[email_index - 1]
        
        # 获取回复内容
        reply_body = custom_message if custom_message else email['reply_draft']
        
        # 获取 Gmail 服务
        service = get_gmail_service()
        
        # 获取原始邮件信息以构造回复
        original = service.users().messages().get(
            userId='me', 
            id=email['id'],
            format='metadata',
            metadataHeaders=['Subject', 'From', 'Message-ID', 'References']
        ).execute()
        
        headers = {h['name'].lower(): h['value'] for h in original.get('payload', {}).get('headers', [])}
        
        original_from = headers.get('from', '')
        original_subject = headers.get('subject', '')
        original_message_id = headers.get('message-id', '')
        original_references = headers.get('references', '')
        
        # 构造回复主题
        if not original_subject.lower().startswith('re:'):
            reply_subject = f"Re: {original_subject}"
        else:
            reply_subject = original_subject
        
        # 构造回复邮件
        # 提取发件人邮箱
        import re
        to_match = re.search(r'<([^>]+)>', original_from)
        to_email = to_match.group(1) if to_match else original_from
        
        # 构造邮件内容
        email_body = f"{reply_body}\n\n---\nOriginal message:\nFrom: {original_from}\nSubject: {original_subject}\n"
        
        # 使用 MIME 格式
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        msg = MIMEMultipart()
        msg['To'] = to_email
        msg['Subject'] = reply_subject
        msg['In-Reply-To'] = original_message_id
        msg['References'] = f"{original_references} {original_message_id}".strip() if original_references else original_message_id
        
        msg.attach(MIMEText(email_body, 'plain', 'utf-8'))
        
        # 编码并发送
        raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
        
        service.users().messages().send(
            userId='me',
            body={'raw': raw_message, 'threadId': original.get('threadId')}
        ).execute()
        
        # 标记原邮件为已回复（可选）
        # service.users().messages().modify(
        #     userId='me',
        #     id=email['id'],
        #     body={'addLabelIds': ['Label_1']}  # 假设有一个"已回复"标签
        # ).execute()
        
        return f"✅ 回复已发送给：{original_from}\n主题：{reply_subject}\n内容：\n{reply_body}"
        
    except Exception as e:
        return f"❌ 发送回复失败: {str(e)}"


def list_pending_replies():
    """列出所有待回复邮件"""
    pending = load_pending_replies()
    if not pending or not pending.get('emails'):
        return "📭 当前没有待回复的邮件"
    
    emails = pending['emails']
    timestamp = pending.get('timestamp', '未知时间')
    
    msg_parts = [f"📧 待回复邮件列表（检查时间: {timestamp}）\n"]
    msg_parts.append(f"共 {len(emails)} 封邮件：\n")
    
    for i, email in enumerate(emails, 1):
        msg_parts.append(f"\n【{i}】{email['subject']}")
        msg_parts.append(f"  发件人: {email['from']}")
        msg_parts.append(f"  建议回复: {email['reply_draft'][:50]}...")
    
    msg_parts.append(f"\n\n💡 使用：回复邮件X [自定义内容]")
    return "\n".join(msg_parts)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 gmail_send_reply.py list          # 列出待回复邮件")
        print("  python3 gmail_send_reply.py send 1        # 发送第1封邮件的默认回复")
        print("  python3 gmail_send_reply.py send 1 '自定义内容'  # 发送自定义回复")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        print(list_pending_replies())
    elif command == 'send' and len(sys.argv) >= 3:
        try:
            index = int(sys.argv[2])
            custom_msg = sys.argv[3] if len(sys.argv) > 3 else None
            print(send_reply(index, custom_msg))
        except ValueError:
            print("❌ 邮件编号必须是数字")
    else:
        print("❌ 无效命令")
