#!/usr/bin/env python3
"""
Gmail 智能检查脚本
- 检查未读邮件
- AI 判断重要邮件
- 生成摘要和回复建议
- 推送至 QQ
"""

import os
import base64
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# Gmail API 权限范围
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.modify']

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
            raise Exception("Gmail 未登录，请先完成 OAuth 授权")
    
    return build('gmail', 'v1', credentials=creds)

def is_important_email(email_data):
    """
    判断邮件是否重要
    基于多种因素：发件人、主题、内容关键词等
    """
    headers = {h['name'].lower(): h['value'] for h in email_data.get('payload', {}).get('headers', [])}
    
    from_email = headers.get('from', '').lower()
    subject = headers.get('subject', '').lower()
    
    # 重要发件人白名单
    important_senders = [
        'noreply@github.com',
        'notifications@github.com',
        'linkedin',
        'recruiting',
        'hr@',
        'offer@',
        'billing@',
        'payment@',
        'bank',
        'scholar.google',
        'journal',
        'conference',
    ]
    
    # 重要关键词
    important_keywords = [
        'offer', '面试', 'interview', '录用', 'hired', 'congratulations',
        'accepted', 'paper', 'review', 'deadline', 'payment', 'invoice',
        'billing', 'subscription', 'security', 'alert', 'important',
        'urgent', 'action required', 'verify', 'confirm',
    ]
    
    # 垃圾邮件关键词
    spam_keywords = [
        'unsubscribe', 'promotion', 'sale', 'discount', 'limited time',
        'marketing', 'newsletter', 'digest', 'notification@youtube',
        'notification@twitter', 'no-reply@medium',
    ]
    
    # 检查是否是重要发件人
    for sender in important_senders:
        if sender in from_email:
            return True, f"重要发件人: {sender}"
    
    # 检查重要关键词
    for keyword in important_keywords:
        if keyword in subject:
            return True, f"关键词匹配: {keyword}"
    
    # 检查垃圾邮件关键词
    spam_score = 0
    for keyword in spam_keywords:
        if keyword in subject or keyword in from_email:
            spam_score += 1
    
    if spam_score >= 2:
        return False, "疑似营销/通知邮件"
    
    # 如果没有明显特征，检查邮件标签
    label_ids = email_data.get('labelIds', [])
    if 'CATEGORY_PERSONAL' in label_ids or 'IMPORTANT' in label_ids:
        return True, "Gmail 标记为重要/个人"
    
    if 'CATEGORY_PROMOTIONS' in label_ids or 'CATEGORY_SOCIAL' in label_ids:
        return False, "Gmail 分类为推广/社交"
    
    # 默认检查：如果是直接的 to: 而不是通过 mailing list
    to_field = headers.get('to', '').lower()
    if 'jokebearbot@gmail.com' in to_field and '+' not in to_field:
        return True, "直接发送给你"
    
    return False, "普通邮件"

def generate_reply_draft(email_data, importance_reason):
    """生成回复草稿（仅建议，需用户确认后才发送）"""
    headers = {h['name'].lower(): h['value'] for h in email_data.get('payload', {}).get('headers', [])}
    
    from_name = headers.get('from', 'Unknown')
    subject = headers.get('subject', 'No Subject')
    
    # 根据不同类型生成不同回复
    if 'github' in from_name.lower():
        draft = f"感谢通知。我会查看相关的 GitHub 更新/PR/issue。"
    elif 'interview' in subject.lower() or '面试' in subject:
        draft = f"感谢您安排面试。请确认时间和平台，我会准时参加。如有需要请随时联系。"
    elif 'offer' in subject.lower() or '录用' in subject:
        draft = f"非常感谢您的录用通知！我会仔细审阅 offer 条款，并在规定时间内回复。"
    elif 'paper' in subject.lower() or 'review' in subject.lower():
        draft = f"感谢您的审稿/投稿通知。我会按要求处理，并在截止日期前完成。"
    else:
        # 通用礼貌回复
        draft = f"感谢您的邮件。我已收到并会尽快处理。如有紧急事项请通过 QQ/微信直接联系。"
    
    return draft


def save_pending_replies(important_emails):
    """保存待回复的重要邮件列表，供用户后续确认"""
    import json
    
    pending_file = '/tmp/gmail_pending_replies.json'
    
    # 只保存必要信息
    pending_data = {
        'timestamp': datetime.now().isoformat(),
        'emails': [
            {
                'id': email['id'],
                'from': email['from'],
                'subject': email['subject'],
                'reply_draft': email['reply_draft'],
                'message_id': email.get('message_id', '')
            }
            for email in important_emails
        ]
    }
    
    with open(pending_file, 'w') as f:
        json.dump(pending_data, f, ensure_ascii=False, indent=2)
    
    return pending_file

def get_email_body(email_data):
    """获取邮件正文"""
    payload = email_data.get('payload', {})
    
    # 尝试获取纯文本内容
    if 'parts' in payload:
        for part in payload['parts']:
            if part.get('mimeType') == 'text/plain':
                data = part.get('body', {}).get('data', '')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')[:500]
            elif part.get('mimeType') == 'text/html':
                data = part.get('body', {}).get('data', '')
                if data:
                    html = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                    # 简单去除 HTML 标签
                    import re
                    text = re.sub('<[^<]+?>', '', html)
                    return text[:500]
    
    # 直接获取 body
    body_data = payload.get('body', {}).get('data', '')
    if body_data:
        return base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')[:500]
    
    return "[无法获取邮件内容]"

def check_gmail():
    """主检查函数
    
    返回结构:
    - important: 重要邮件列表（详细通知）
    - unimportant: 不重要邮件汇总信息
    - spam: 垃圾邮件数量（完全忽略，不计入通知）
    """
    try:
        service = get_gmail_service()
        
        # 获取未读邮件（最近24小时）
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d')
        query = f'is:unread after:{yesterday}'
        
        results = service.users().messages().list(
            userId='me', 
            q=query,
            maxResults=30
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            return {'important': [], 'unimportant': [], 'spam_count': 0}  # 没有新邮件
        
        important_emails = []
        unimportant_summary = {
            'count': 0,
            'categories': {
                'social': [],      # 社交媒体通知
                'promotion': [],   # 促销/营销
                'notification': [], # 系统通知
                'other': []        # 其他普通邮件
            }
        }
        spam_count = 0
        
        for msg in messages:
            email_data = service.users().messages().get(
                userId='me', 
                id=msg['id'],
                format='full'
            ).execute()
            
            is_important, reason = is_important_email(email_data)
            
            if is_important:
                headers = {h['name'].lower(): h['value'] for h in email_data.get('payload', {}).get('headers', [])}
                
                email_info = {
                    'id': msg['id'],
                    'from': headers.get('from', 'Unknown'),
                    'subject': headers.get('subject', 'No Subject'),
                    'date': headers.get('date', ''),
                    'snippet': email_data.get('snippet', ''),
                    'body_preview': get_email_body(email_data),
                    'importance_reason': reason,
                    'reply_draft': generate_reply_draft(email_data, reason),
                    'message_id': headers.get('message-id', '')
                }
                important_emails.append(email_info)
            else:
                # 不重要邮件，分类汇总
                category = categorize_unimportant_email(email_data, reason)
                
                if category == 'spam':
                    spam_count += 1
                else:
                    headers = {h['name'].lower(): h['value'] for h in email_data.get('payload', {}).get('headers', [])}
                    unimportant_summary['count'] += 1
                    unimportant_summary['categories'][category].append({
                        'from': headers.get('from', 'Unknown').split('<')[0].strip()[:30],  # 只取名字部分
                        'subject': headers.get('subject', 'No Subject')[:40]  # 截断主题
                    })
        
        # 如果有重要邮件，保存待回复列表
        if important_emails:
            save_pending_replies(important_emails)
        
        return {
            'important': important_emails,
            'unimportant': unimportant_summary,
            'spam_count': spam_count
        }
        
    except Exception as e:
        return {'error': str(e)}


def categorize_unimportant_email(email_data, reason):
    """
    对不重要邮件进行分类
    
    返回: 'social', 'promotion', 'notification', 'other', 'spam'
    """
    headers = {h['name'].lower(): h['value'] for h in email_data.get('payload', {}).get('headers', [])}
    from_email = headers.get('from', '').lower()
    subject = headers.get('subject', '').lower()
    label_ids = email_data.get('labelIds', [])
    
    # 明显的垃圾/推销邮件特征
    spam_signals = [
        'unsubscribe', '促销', '优惠', '打折', '限时', '抢购',
        '免费领', '中奖', '恭喜您', '赢取', '现金红包'
    ]
    spam_score = sum(1 for signal in spam_signals if signal in subject)
    
    if spam_score >= 2 or 'CATEGORY_PROMOTIONS' in label_ids and any(x in subject for x in ['sale', 'discount', '% off']):
        return 'spam'
    
    # 社交媒体通知
    social_senders = ['facebook', 'twitter', 'instagram', 'youtube', 'tiktok', 'snapchat', 'pinterest']
    if any(s in from_email for s in social_senders) or 'CATEGORY_SOCIAL' in label_ids:
        return 'social'
    
    # 促销/营销
    promo_signals = ['promotion', 'sale', 'newsletter', 'digest', 'subscribe', '订阅']
    if any(s in from_email or s in subject for s in promo_signals) or 'CATEGORY_PROMOTIONS' in label_ids:
        return 'promotion'
    
    # 系统通知
    notification_senders = ['notifications@', 'noreply@', 'no-reply@', 'alert@', 'info@']
    if any(s in from_email for s in notification_senders):
        return 'notification'
    
    return 'other'

def format_notification(result, check_time=""):
    """格式化通知消息
    
    处理三种情况：
    1. 有重要邮件 - 详细展示
    2. 只有不重要邮件 - 汇总展示  
    3. 只有垃圾邮件 - 告知已过滤
    4. 没有新邮件 - 简单提示
    """
    # 错误处理
    if isinstance(result, dict) and 'error' in result:
        return f"📧 {check_time} Gmail 检查\n\n❌ 检查出错: {result['error']}"
    
    important = result.get('important', [])
    unimportant = result.get('unimportant', {'count': 0, 'categories': {}})
    spam_count = result.get('spam_count', 0)
    
    total_unread = len(important) + unimportant['count'] + spam_count
    
    if total_unread == 0:
        return f"📧 {check_time} Gmail 检查\n\n✅ 没有新邮件"
    
    # 开始构建消息
    msg_parts = [f"📧 {check_time} Gmail 检查\n"]
    msg_parts.append(f"未读邮件共 {total_unread} 封：")
    msg_parts.append(f"  📌 重要: {len(important)} 封")
    if unimportant['count'] > 0:
        msg_parts.append(f"  📬 其他: {unimportant['count']} 封")
    if spam_count > 0:
        msg_parts.append(f"  🗑️ 垃圾邮件: {spam_count} 封（已过滤）")
    
    # 重要邮件详细展示
    if important:
        msg_parts.append(f"\n{'═' * 40}")
        msg_parts.append("📌 重要邮件详情：")
        
        for i, email in enumerate(important, 1):
            msg_parts.append(f"\n{'─' * 40}")
            msg_parts.append(f"【{i}】{email['subject']}")
            msg_parts.append(f"发件人: {email['from']}")
            msg_parts.append(f"判断依据: {email['importance_reason']}")
            msg_parts.append(f"\n💬 回复建议:")
            msg_parts.append(f"{email['reply_draft']}")
        
        msg_parts.append(f"\n{'─' * 40}")
        msg_parts.append("\n⚠️ 以上为回复建议草稿，需要你先确认")
        msg_parts.append("💡 如需回复，请告诉我：「回复邮件X」+ 修改意见（可选）")
    
    # 不重要邮件汇总
    if unimportant['count'] > 0:
        msg_parts.append(f"\n{'═' * 40}")
        msg_parts.append("📬 其他邮件汇总：")
        
        cats = unimportant['categories']
        
        if cats['social']:
            msg_parts.append(f"\n📱 社交媒体 ({len(cats['social'])} 封):")
            for email in cats['social'][:3]:  # 最多显示3封
                msg_parts.append(f"  - {email['from']}: {email['subject']}")
            if len(cats['social']) > 3:
                msg_parts.append(f"  ... 还有 {len(cats['social']) - 3} 封")
        
        if cats['promotion']:
            msg_parts.append(f"\n🛍️ 促销/营销 ({len(cats['promotion'])} 封):")
            for email in cats['promotion'][:2]:
                msg_parts.append(f"  - {email['from']}")
            if len(cats['promotion']) > 2:
                msg_parts.append(f"  ... 还有 {len(cats['promotion']) - 2} 封")
        
        if cats['notification']:
            msg_parts.append(f"\n🔔 系统通知 ({len(cats['notification'])} 封):")
            for email in cats['notification'][:2]:
                msg_parts.append(f"  - {email['from']}: {email['subject']}")
            if len(cats['notification']) > 2:
                msg_parts.append(f"  ... 还有 {len(cats['notification']) - 2} 封")
        
        if cats['other']:
            msg_parts.append(f"\n📨 其他邮件 ({len(cats['other'])} 封):")
            for email in cats['other'][:2]:
                msg_parts.append(f"  - {email['from']}: {email['subject']}")
            if len(cats['other']) > 2:
                msg_parts.append(f"  ... 还有 {len(cats['other']) - 2} 封")
    
    return "\n".join(msg_parts)

if __name__ == "__main__":
    emails = check_gmail()
    now = datetime.now().strftime("%m/%d %H:%M")
    notification = format_notification(emails, now)
    print(notification)
