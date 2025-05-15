#!/usr/bin/env python3
"""
自动生成CHANGELOG.md的工具

这个脚本会根据git提交记录自动生成或更新CHANGELOG.md文件。
使用规范化的提交消息格式（Conventional Commits）可以获得更好的结果。

规范化提交消息格式:
- feat: 新功能
- fix: 修复bug
- docs: 文档变更
- style: 代码风格变更，不影响代码功能
- refactor: 代码重构，不添加新功能也不修复bug
- perf: 性能优化
- test: 添加或修改测试代码
- build: 构建系统或外部依赖变更
- ci: CI配置或脚本变更
- chore: 其他变更，不修改src或测试文件

使用方法:
    python tools/generate_changelog.py
"""

import subprocess
import re
import os
import datetime
from collections import defaultdict

# 获取版本号从pyproject.toml
def get_current_version():
    with open('pyproject.toml', 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('version'):
                return line.split('=')[1].strip().strip('"\'')
    return '未知版本'

# 获取最后一个tag或版本
def get_last_version():
    try:
        # 尝试获取最近的tag
        result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'], 
                               capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        # 如果没有tag，则获取第一次提交
        result = subprocess.run(['git', 'rev-list', '--max-parents=0', 'HEAD'], 
                               capture_output=True, text=True, check=True)
        return result.stdout.strip()

# 获取提交记录
def get_commits(since_revision):
    cmd = ['git', 'log', f'{since_revision}..HEAD', '--pretty=format:%s|%h|%an|%ad', '--date=short']
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    
    if not result.stdout:
        return []
        
    commits = []
    for line in result.stdout.splitlines():
        parts = line.split('|')
        if len(parts) >= 4:
            message, commit_hash, author, date = parts[0], parts[1], parts[2], parts[3]
            commits.append({
                'message': message,
                'hash': commit_hash,
                'author': author,
                'date': date
            })
    return commits

# 解析提交消息
def parse_commit_message(message):
    # 匹配规范化提交消息
    pattern = r'^(?P<type>feat|fix|docs|style|refactor|perf|test|build|ci|chore)(?:\((?P<scope>[^)]+)\))?: (?P<message>.+)$'
    match = re.match(pattern, message)
    
    if match:
        result = match.groupdict()
        # 检查是否有破坏性变更标记
        if '!' in result['type'] or 'BREAKING CHANGE' in message:
            result['breaking'] = True
        else:
            result['breaking'] = False
        return result
    
    # 非规范化提交，尝试一般性分类
    if 'fix' in message.lower() or 'bug' in message.lower() or '修复' in message:
        return {'type': 'fix', 'scope': None, 'message': message, 'breaking': False}
    elif 'add' in message.lower() or 'new' in message.lower() or '新增' in message or '添加' in message:
        return {'type': 'feat', 'scope': None, 'message': message, 'breaking': False}
    elif 'doc' in message.lower() or '文档' in message:
        return {'type': 'docs', 'scope': None, 'message': message, 'breaking': False}
    elif 'test' in message.lower() or '测试' in message:
        return {'type': 'test', 'scope': None, 'message': message, 'breaking': False}
    elif 'refactor' in message.lower() or '重构' in message:
        return {'type': 'refactor', 'scope': None, 'message': message, 'breaking': False}
    elif 'style' in message.lower() or '格式' in message or '样式' in message:
        return {'type': 'style', 'scope': None, 'message': message, 'breaking': False}
    else:
        return {'type': 'other', 'scope': None, 'message': message, 'breaking': False}

# 生成日志内容
def generate_changelog_content(commits, version):
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    # 初始化各类型变更
    changes = defaultdict(list)
    
    # 分类提交
    for commit in commits:
        parsed = parse_commit_message(commit['message'])
        
        # 特殊处理规范化提交
        if parsed['type'] == 'feat':
            changes['新增'].append(f"- {parsed['message']} ({commit['hash']})")
        elif parsed['type'] == 'fix':
            changes['修复'].append(f"- {parsed['message']} ({commit['hash']})")
        elif parsed['type'] == 'docs':
            changes['文档'].append(f"- {parsed['message']} ({commit['hash']})")
        elif parsed['type'] in ['refactor', 'style', 'perf']:
            changes['优化'].append(f"- {parsed['message']} ({commit['hash']})")
        elif parsed['type'] in ['test', 'build', 'ci']:
            changes['其他'].append(f"- {parsed['message']} ({commit['hash']})")
        elif parsed['type'] == 'chore':
            changes['其他'].append(f"- {parsed['message']} ({commit['hash']})")
        else:
            changes['其他'].append(f"- {commit['message']} ({commit['hash']})")
    
    # 生成内容
    content = f"\n## [{version}] - {today}\n\n"
    
    # 添加分类内容
    for section, items in changes.items():
        if items:
            content += f"### {section}\n"
            content += "\n".join(items)
            content += "\n\n"
    
    return content

# 更新CHANGELOG文件
def update_changelog(content):
    changelog_path = 'CHANGELOG.md'
    header = "# 更新日志\n\n本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/) 和 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/) 规范。\n"
    
    if os.path.exists(changelog_path):
        with open(changelog_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
            
        # 如果已有header，不要重复添加
        if existing_content.startswith(header.strip()):
            # 在header后面插入新内容
            parts = existing_content.split('\n\n', 1)
            if len(parts) > 1:
                updated_content = parts[0] + '\n\n' + content + parts[1]
            else:
                updated_content = parts[0] + '\n\n' + content
        else:
            updated_content = header + content + existing_content
    else:
        updated_content = header + content
    
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"已更新 {changelog_path}")

def main():
    try:
        last_version = get_last_version()
        current_version = get_current_version()
        
        print(f"正在生成从 {last_version} 到 {current_version} 的更新日志...")
        
        commits = get_commits(last_version)
        if not commits:
            print("未找到新的提交记录")
            return
            
        content = generate_changelog_content(commits, current_version)
        update_changelog(content)
        
    except subprocess.CalledProcessError as e:
        print(f"错误: {e}")
        print(f"命令输出: {e.output}")
        

if __name__ == "__main__":
    main() 