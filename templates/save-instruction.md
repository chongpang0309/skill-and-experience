# 保存到 GitHub 指令

当用户说以下类似话语时，需要保存内容到本仓库：

## 触发词
- "保存到 GitHub"
- "保存到仓库"
- "提交到 GitHub"
- "保存这个"
- "记下来"
- "存到 skill-and-experience"

## 处理流程

1. **分析内容类型**
   - 技能学习 → `skills/` 下的对应子目录
   - 项目经验 → `experiences/projects/`
   - 问题解决 → `experiences/problems/`
   - 心得体会 → `experiences/insights/`
   - 临时笔记 → `notes/`

2. **确定子目录**
   - 检查是否已有相关子目录
   - 没有则创建新的子目录（使用小写字母和连字符）

3. **生成文件名**
   - 基于内容主题
   - 格式：`主题-简要描述.md`
   - 如有日期相关信息，可加上 `YYYY-MM-DD-`

4. **格式化内容**
   - 转换为 Markdown 格式
   - 添加适当的标题和结构
   - 添加创建日期

5. **Git 操作**
   - 保存文件到正确位置
   - `git add .`
   - `git commit -m "描述: 文件主题"`
   - `git push origin main`

6. **整理检查**
   - 当文件数量超过 20 个时，提醒用户进行整理
   - 定期（每月）检查目录结构，建议归档旧文件

## 示例

用户："保存到 GitHub，我今天学会了怎么用 Docker"

操作：
1. 类型：技能学习 → `skills/tools/`
2. 文件名：`docker-basics.md`
3. 提交信息：`add: Docker 基础使用指南`
