# 自动化发布方案A - 实施指南

> 方案：wechat-publisher + xiaohongshu-publish 专业组合
> 目标：每天自动发布文章到公众号和小红书

---

## 📦 技能信息

### 1. wechat-publisher（微信公众号发布）
- **版本**：0.1.0
- **作者**：0731coderlee-sudo
- **功能**：一键发布 Markdown 到微信公众号草稿箱
- **技术**：基于 wenyan-cli，支持多主题、代码高亮、图片自动上传
- **来源**：clawhub 公共仓库

### 2. xiaohongshu-publish（小红书长文发布）
- **版本**：1.0.0
- **作者**：enjoytdl
- **功能**：小红书长文发布，支持网页版小红书创作服务平台
- **来源**：clawhub 公共仓库

---

## 🛠️ 安装步骤

### 第一步：安装技能（等速率限制恢复后执行）

```bash
# 安装公众号发布技能
clawhub install wechat-publisher --dir /root/.openclaw/workspace/skills

# 安装小红书发布技能
clawhub install xiaohongshu-publish --dir /root/.openclaw/workspace/skills
```

### 第二步：查看技能文档

安装完成后，阅读 SKILL.md 了解使用方法：

```bash
cat /root/.openclaw/workspace/skills/wechat-publisher/SKILL.md
cat /root/.openclaw/workspace/skills/xiaohongshu-publish/SKILL.md
```

---

## ⚙️ 配置要求

### 1. 微信公众号配置

#### 需要准备的凭证：
- [ ] 公众号账号（邮箱/微信号）
- [ ] 密码
- [ ] 管理员微信扫码认证（首次登录需要）

#### 登录方式选择：

**方式A：Cookie登录（推荐）**
- 优点：一次配置，长期使用
- 缺点：Cookie会过期（约1-3个月），需要更新

**方式B：扫码登录**
- 优点：更安全
- 缺点：每次发布都需要扫码

### 2. 小红书配置

#### 需要准备的凭证：
- [ ] 小红书账号（手机号/邮箱）
- [ ] 密码
- [ ] 创作者平台权限（需先申请成为创作者）

#### 登录方式：
- 网页版登录
- 需要保持登录状态

---

## 📁 内容准备规范

### 文件目录结构

```
content/
├── articles/                    # 文章库
│   ├── wechat/                 # 公众号文章（长文）
│   │   ├── 001-weekly-report.md
│   │   ├── 002-dev-tools.md
│   │   └── 003-ppt.md
│   └── xiaohongshu/            # 小红书文章（短文+多图）
│       ├── 001-weekly-report/
│       │   ├── text.md         # 正文
│       │   ├── cover.jpg       # 封面图
│       │   └── images/         # 配图
│       └── ...
├── schedule.json               # 发布计划
└── published.json              # 已发布记录
```

### 文章格式规范

#### 公众号文章（Markdown）

```markdown
---
title: 如何用AI一天写完周报：我的完整workflow
cover: ./images/cover-001.jpg
tags: [AI, 职场效率, 周报]
author: 两天的AI笔记
date: 2025-03-10
---

# 正文内容...

## 前言
...
```

#### 小红书文章（结构化）

```json
{
  "title": "如何用AI一天写完周报",
  "content": "正文内容（500-1000字）",
  "cover": "./images/cover-001.jpg",
  "images": [
    "./images/step1.jpg",
    "./images/step2.jpg",
    "./images/step3.jpg"
  ],
  "tags": ["AI", "职场", "效率工具"],
  "location": "",
  "topic": "职场干货"
}
```

---

## 🔄 发布流程设计

### 自动化流程图

```
定时触发（每天9:00）
    ↓
读取发布计划（schedule.json）
    ↓
检查今日是否有待发布文章
    ↓
是 → 读取文章内容
    ↓
格式转换（Markdown → 平台格式）
    ↓
上传图片到平台
    ↓
发布到公众号草稿箱
    ↓
发布到小红书
    ↓
记录发布状态
    ↓
发送通知（成功/失败）
```

### 发布计划示例（schedule.json）

```json
{
  "schedule": [
    {
      "date": "2025-03-11",
      "wechat": {
        "article": "articles/wechat/001-weekly-report.md",
        "publishTime": "09:00",
        "status": "pending"
      },
      "xiaohongshu": {
        "article": "articles/xiaohongshu/001-weekly-report",
        "publishTime": "09:30",
        "status": "pending"
      }
    },
    {
      "date": "2025-03-13",
      "wechat": {
        "article": "articles/wechat/002-dev-tools.md",
        "publishTime": "09:00",
        "status": "pending"
      },
      "xiaohongshu": {
        "article": "articles/xiaohongshu/002-dev-tools",
        "publishTime": "09:30",
        "status": "pending"
      }
    }
  ],
  "settings": {
    "timezone": "Asia/Shanghai",
    "wechat": {
      "autoPublish": false,
      "saveToDraft": true
    },
    "xiaohongshu": {
      "autoPublish": false,
      "saveToDraft": true
    }
  }
}
```

---

## ⏰ 定时任务配置

### 使用 OpenClaw Cron 设置定时任务

```json
{
  "action": "add",
  "job": {
    "name": "daily-content-publish",
    "schedule": {
      "kind": "cron",
      "expr": "0 9 * * *",
      "tz": "Asia/Shanghai"
    },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "执行每日内容发布任务。读取 /root/.openclaw/workspace/content/schedule.json，检查今日待发布文章，依次发布到公众号和小红书。完成后发送执行报告。",
      "deliver": true,
      "channel": "qqbot",
      "to": "00E5BDBC4E93785FED741E759485DDFA"
    }
  }
}
```

### 手动执行命令

```bash
# 执行发布脚本
cd /root/.openclaw/workspace
python3 scripts/publish_daily.py
```

---

## 📝 发布脚本示例

### publish_daily.py

```python
#!/usr/bin/env python3
"""
每日内容发布脚本
自动发布文章到公众号和小红书
"""

import json
import os
from datetime import datetime

def load_schedule():
    """加载发布计划"""
    with open('content/schedule.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_today_article(schedule):
    """获取今日待发布文章"""
    today = datetime.now().strftime('%Y-%m-%d')
    for item in schedule['schedule']:
        if item['date'] == today:
            return item
    return None

def publish_to_wechat(article_path):
    """发布到公众号"""
    # 调用 wechat-publisher 技能
    cmd = f"openclaw skills wechat-publisher publish {article_path}"
    result = os.system(cmd)
    return result == 0

def publish_to_xiaohongshu(article_path):
    """发布到小红书"""
    # 调用 xiaohongshu-publish 技能
    cmd = f"openclaw skills xiaohongshu-publish publish {article_path}"
    result = os.system(cmd)
    return result == 0

def main():
    """主函数"""
    print(f"[{datetime.now()}] 开始执行每日发布任务...")
    
    # 加载计划
    schedule = load_schedule()
    today_article = get_today_article(schedule)
    
    if not today_article:
        print("今日无待发布文章")
        return
    
    # 发布到公众号
    if today_article.get('wechat'):
        print(f"正在发布公众号文章: {today_article['wechat']['article']}")
        success = publish_to_wechat(today_article['wechat']['article'])
        print(f"公众号发布: {'成功' if success else '失败'}")
    
    # 发布到小红书
    if today_article.get('xiaohongshu'):
        print(f"正在发布小红书文章: {today_article['xiaohongshu']['article']}")
        success = publish_to_xiaohongshu(today_article['xiaohongshu']['article'])
        print(f"小红书发布: {'成功' if success else '失败'}")
    
    print(f"[{datetime.now()}] 发布任务完成")

if __name__ == '__main__':
    main()
```

---

## 🔐 安全与风险

### 账号安全

1. **使用专用账号**
   - 建议注册专门用于自动化的子账号
   - 不要用在用的主账号

2. **定期更换密码**
   - 每3个月更换一次密码
   - 启用两步验证

3. **登录状态监控**
   - 设置登录失效检测
   - 失效时发送通知

### 平台风控规避

1. **控制发布频率**
   - 公众号：每天最多1篇
   - 小红书：每天最多2-3篇
   - 避免短时间内大量发布

2. **模拟人工操作**
   - 添加随机延迟（5-30秒）
   - 模拟鼠标移动和点击
   - 使用正常的User-Agent

3. **内容合规检查**
   - 自动检测敏感词
   - 确保内容符合平台规范
   - 避免被判定为营销号

---

## 📊 监控与日志

### 日志记录

```python
# 发布日志格式
{
  "timestamp": "2025-03-10T09:00:00+08:00",
  "platform": "wechat",
  "article": "001-weekly-report.md",
  "status": "success",
  "message": "发布成功",
  "url": "https://mp.weixin.qq.com/..."
}
```

### 通知机制

发布完成后，通过QQ发送通知：

```
✅ 今日发布完成

公众号：《如何用AI一天写完周报》
状态：已发布
链接：https://mp.weixin.qq.com/...

小红书：《如何用AI一天写完周报》
状态：已发布
链接：https://www.xiaohongshu.com/...

下次发布：2025-03-13 09:00
```

---

## 🚀 实施时间表

| 阶段 | 时间 | 任务 |
|------|------|------|
| **第1天** | 2小时 | 安装技能，配置环境 |
| **第2天** | 2小时 | 准备账号，测试登录 |
| **第3天** | 3小时 | 准备首批内容，测试发布 |
| **第4天** | 2小时 | 配置定时任务，完善脚本 |
| **第5天** | 1小时 | 正式上线，监控运行 |

---

## 📞 问题排查

### 常见问题

1. **登录失败**
   - 检查账号密码
   - 确认是否需要验证码
   - 检查Cookie是否过期

2. **发布失败**
   - 检查文章格式是否正确
   - 检查图片路径是否正确
   - 查看平台是否有新限制

3. **定时任务不执行**
   - 检查Cron表达式
   - 检查时区设置
   - 检查OpenClaw服务状态

---

## ✅ 检查清单

### 安装前检查

- [ ] 已注册微信公众号
- [ ] 已注册小红书创作者账号
- [ ] 服务器/电脑可24小时运行（或定时启动）
- [ ] 已安装Chrome浏览器
- [ ] 网络可访问公众号和小红书

### 安装后检查

- [ ] 技能安装成功
- [ ] 可正常登录公众号
- [ ] 可正常登录小红书
- [ ] 可成功发布测试文章
- [ ] 定时任务配置正确
- [ ] 通知机制正常工作

---

## 📝 更新记录

- 2025-03-10: 创建方案A实施指南

---

**下一步：等待clawhub速率限制恢复后，执行安装命令**
