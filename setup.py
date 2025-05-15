#!/usr/bin/env python3
"""
计划管理工具 - 安装脚本
"""

from setuptools import setup, find_packages

# 读取README文件内容作为长描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="plan-manager",  
    version="1.0.0",
    author="麦咪", 
    author_email="maimai@example.com", 
    description="一个简单的计划管理工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/plan-manager",  
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "plan-manager=plan_manager.main:main",
            "plan-manager-gui=plan_manager.main:main_gui",
        ],
    },
    scripts=[
        "plan_manager/bin/plan-manager",
        "plan_manager/bin/plan-manager-gui",
    ],
    install_requires=[
        # 依赖包，本项目只使用标准库
    ],
) 