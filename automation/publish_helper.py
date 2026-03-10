#!/usr/bin/env python3
"""
内容发布辅助脚本 - 方案A备用
在自动化技能安装完成前，使用此脚本辅助手动发布
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_schedule():
    """加载发布计划"""
    schedule_path = Path('/root/.openclaw/workspace/content/schedule.json')
    if not schedule_path.exists():
        print("错误：找不到发布计划文件")
        return None
    
    with open(schedule_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_today_article(schedule):
    """获取今日待发布文章"""
    today = datetime.now().strftime('%Y-%m-%d')
    for item in schedule.get('schedule', []):
        if item.get('date') == today:
            return item
    return None

def format_wechat_article(article_path):
    """格式化公众号文章（转换为微信编辑器可用格式）"""
    if not os.path.exists(article_path):
        return None, f"文件不存在: {article_path}"
    
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题
    title = ""
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            title = line.replace('# ', '').strip()
            break
    
    # 转换Markdown为微信格式（简化版）
    wechat_content = content
    
    # 简单的格式转换
    wechat_content = wechat_content.replace('# ', '## ')  # 标题降级
    wechat_content = wechat_content.replace('## ', '### ')
    wechat_content = wechat_content.replace('```', '')   # 移除代码块标记
    
    return {
        'title': title,
        'content': wechat_content,
        'source_path': article_path
    }, None

def format_xiaohongshu_article(article_dir):
    """格式化小红书文章"""
    article_path = Path(article_dir)
    
    # 读取正文
    text_file = article_path / 'text.md'
    if not text_file.exists():
        return None, f"找不到正文文件: {text_file}"
    
    with open(text_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 读取配置
    config_file = article_path / 'config.json'
    config = {}
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    
    # 查找图片
    images = []
    images_dir = article_path / 'images'
    if images_dir.exists():
        for img in sorted(images_dir.glob('*')):
            if img.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                images.append(str(img))
    
    # 查找封面
    cover = article_path / 'cover.jpg'
    if not cover.exists():
        cover = article_path / 'cover.png'
    
    return {
        'title': config.get('title', '无标题'),
        'content': content,
        'cover': str(cover) if cover.exists() else None,
        'images': images,
        'tags': config.get('tags', []),
        'source_path': str(article_path)
    }, None

def generate_publish_guide(wechat_article=None, xhs_article=None):
    """生成发布指南"""
    guide = []
    
    guide.append("=" * 60)
    guide.append("📢 今日内容发布指南")
    guide.append(f"📅 日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    guide.append("=" * 60)
    guide.append("")
    
    if wechat_article:
        guide.append("📱 微信公众号发布")
        guide.append("-" * 40)
        guide.append(f"标题: {wechat_article['title']}")
        guide.append(f"来源: {wechat_article['source_path']}")
        guide.append("")
        guide.append("操作步骤:")
        guide.append("1. 登录公众号后台: https://mp.weixin.qq.com")
        guide.append("2. 点击「新的创作」→「图文消息」")
        guide.append(f"3. 复制以下内容到编辑器:")
        guide.append("")
        guide.append("--- 正文开始 ---")
        guide.append(wechat_article['content'][:500] + "...")  # 只显示前500字
        guide.append("--- 正文结束 ---")
        guide.append("")
        guide.append("4. 设置封面图")
        guide.append("5. 保存并发布")
        guide.append("")
    
    if xhs_article:
        guide.append("📕 小红书发布")
        guide.append("-" * 40)
        guide.append(f"标题: {xhs_article['title']}")
        guide.append(f"来源: {xhs_article['source_path']}")
        guide.append(f"封面: {xhs_article['cover']}")
        guide.append(f"配图: {len(xhs_article['images'])} 张")
        guide.append(f"标签: {', '.join(xhs_article['tags'])}")
        guide.append("")
        guide.append("操作步骤:")
        guide.append("1. 登录小红书创作服务平台: https://creator.xiaohongshu.com")
        guide.append("2. 点击「发布笔记」")
        guide.append("3. 上传封面图和配图")
        guide.append("4. 填写标题和正文")
        guide.append("5. 添加标签")
        guide.append("6. 发布")
        guide.append("")
        guide.append("--- 正文 ---")
        guide.append(xhs_article['content'])
        guide.append("")
    
    guide.append("=" * 60)
    guide.append("✅ 发布完成后，记得更新 schedule.json 中的状态")
    guide.append("=" * 60)
    
    return '\n'.join(guide)

def main():
    """主函数"""
    print("🚀 内容发布辅助脚本")
    print("")
    
    # 加载发布计划
    schedule = load_schedule()
    if not schedule:
        return
    
    # 获取今日文章
    today_article = get_today_article(schedule)
    if not today_article:
        print("📭 今日没有待发布的内容")
        return
    
    print(f"📅 找到今日发布计划: {today_article.get('date')}")
    print("")
    
    wechat_article = None
    xhs_article = None
    
    # 处理公众号文章
    if 'wechat' in today_article:
        article_path = today_article['wechat'].get('article')
        if article_path:
            print(f"📝 正在处理公众号文章: {article_path}")
            wechat_article, error = format_wechat_article(article_path)
            if error:
                print(f"❌ 公众号文章处理失败: {error}")
            else:
                print(f"✅ 公众号文章已格式化: {wechat_article['title']}")
    
    # 处理小红书文章
    if 'xiaohongshu' in today_article:
        article_dir = today_article['xiaohongshu'].get('article')
        if article_dir:
            print(f"📝 正在处理小红书文章: {article_dir}")
            xhs_article, error = format_xiaohongshu_article(article_dir)
            if error:
                print(f"❌ 小红书文章处理失败: {error}")
            else:
                print(f"✅ 小红书文章已格式化: {xhs_article['title']}")
    
    print("")
    print("=" * 60)
    print("正在生成发布指南...")
    print("=" * 60)
    print("")
    
    # 生成发布指南
    guide = generate_publish_guide(wechat_article, xhs_article)
    
    # 保存到文件
    output_path = Path('/root/.openclaw/workspace/content/publish-guide.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(guide)
    
    # 显示指南
    print(guide)
    print("")
    print(f"💾 发布指南已保存到: {output_path}")
    print("")
    print("🎯 下一步:")
    print("1. 按照上述指南手动发布内容")
    print("2. 发布完成后，更新 schedule.json 中的状态")
    print("3. 等待自动化技能安装完成后，即可自动发布")

if __name__ == '__main__':
    main()
