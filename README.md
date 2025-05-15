# 计划管理工具 (Plan Manager)

![CI Status](https://github.com/Larch-C/plan-manager/actions/workflows/ci.yml/badge.svg)(https://github.com/Larch-C/plan-manager/actions/workflows/ci.yml)
![Release Status](https://github.com/Larch-C/plan-manager/actions/workflows/release.yml/badge.svg)(https://github.com/Larch-C/plan-manager/actions/workflows/release.yml)
![Documentation Status](https://github.com/Larch-C/plan-manager/actions/workflows/docs.yml/badge.svg)(https://github.com/Larch-C/plan-manager/actions/workflows/docs.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

> [!WARNING]
> **注意**：本仓库主要用于学习GitHub Actions工作流运行，不追求实用性，不确保构建的工具可以正常使用。

## 工作流学习目的

本仓库实现了以下GitHub Actions工作流，用于演示和学习CI/CD流程：

1. **CI工作流** (ci.yml)
   - 自动代码格式化和风格检查
   - 多Python版本兼容性测试
   - 使用pre-commit进行代码质量控制
   - 自动修复并提交代码风格问题

2. **发布工作流** (release.yml)
   - 自动版本号管理
   - 基于Git提交记录生成更新日志
   - 构建Python包
   - 发布到PyPI

3. **文档工作流** (docs.yml)
   - 自动构建项目文档
   - 部署到GitHub Pages
   - 根据README和CHANGELOG更新文档

4. **钩子设置工作流** (setup-hooks.yml)
   - 自动设置Git钩子
   - 维护贡献指南
   - 确保提交消息符合约定式提交规范

这些工作流展示了自动化软件开发流程的各个环节，适合学习GitHub Actions的配置和使用。

---

# Plan Manager

![CI Status](https://github.com/Larch-C/plan-manager/actions/workflows/ci.yml/badge.svg)(https://github.com/Larch-C/plan-manager/actions/workflows/ci.yml)
![Release Status](https://github.com/Larch-C/plan-manager/actions/workflows/release.yml/badge.svg)(https://github.com/Larch-C/plan-manager/actions/workflows/release.yml)
![Documentation Status](https://github.com/Larch-C/plan-manager/actions/workflows/docs.yml/badge.svg)(https://github.com/Larch-C/plan-manager/actions/workflows/docs.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

> [!WARNING]
> **Note**: This repository is primarily for learning GitHub Actions workflows, not for practical use. There is no guarantee that the built tools will work properly.

## Workflow Learning Purpose

This repository implements the following GitHub Actions workflows to demonstrate and learn CI/CD processes:

1. **CI Workflow** (ci.yml)
   - Automatic code formatting and style checking
   - Multi-Python version compatibility testing
   - Code quality control using pre-commit
   - Automatic fixing and committing of code style issues

2. **Release Workflow** (release.yml)
   - Automatic version number management
   - Update log generation based on Git commit records
   - Python package building
   - Publishing to PyPI

3. **Documentation Workflow** (docs.yml)
   - Automatic project documentation building
   - Deployment to GitHub Pages
   - Documentation updates based on README and CHANGELOG

4. **Hook Setup Workflow** (setup-hooks.yml)
   - Automatic Git hook setup
   - Maintenance of contribution guidelines
   - Ensuring commit messages conform to conventional commit standards

These workflows demonstrate various aspects of automated software development processes, suitable for learning GitHub Actions configuration and usage.

---

这是一个简单的计划管理工具，可以帮助你存储、管理和跟踪各种计划任务。

## 功能特点

- 添加、更新、删除和查看计划
- 设置计划优先级（低、中、高）
- 添加标签以便分类管理
- 设置截止日期
- 查看即将到期的计划
- 标记计划为已完成
- 通过多种条件筛选计划
- 支持命令行和图形界面两种方式使用

查看 [更新日志](CHANGELOG.md) 获取各版本详细功能列表与改动说明。

This is a simple plan management tool that helps you store, manage, and track various planned tasks.

## Features

- Add, update, delete, and view plans
- Set plan priorities (low, medium, high)
- Add tags for category management
- Set deadlines
- View upcoming plans
- Mark plans as completed
- Filter plans by multiple conditions
- Support both command line and graphical interface usage

See the [Changelog](CHANGELOG.md) for detailed feature lists and modifications for each version.

## 项目结构 | Project Structure

```
plan_manager/
├── plan_manager/          # 包目录 | Package directory
│   ├── __init__.py        # 包初始化文件 | Package initialization file
│   ├── main.py            # 主程序入口 | Main program entry
│   ├── models/            # 数据模型 | Data models
│   │   ├── __init__.py
│   │   └── plan.py        # 计划数据模型 | Plan data model
│   ├── core/              # 核心功能 | Core functionality
│   │   ├── __init__.py
│   │   └── manager.py     # 计划管理器 | Plan manager
│   ├── cli/               # 命令行接口 | Command line interface
│   │   ├── __init__.py
│   │   └── main.py        # 命令行入口 | CLI entry
│   ├── gui/               # 图形界面 | Graphical interface
│   │   ├── __init__.py
│   │   └── app.py         # GUI应用 | GUI application
│   ├── utils/             # 工具函数 | Utility functions
│   │   ├── __init__.py
│   │   └── formatters.py  # 格式化工具 | Formatting tools
│   └── bin/               # 可执行脚本 | Executable scripts
│       ├── plan-manager      # 命令行启动脚本 | CLI startup script
│       └── plan-manager-gui  # GUI启动脚本 | GUI startup script
├── pyproject.toml         # 项目配置文件 | Project configuration file
├── requirements/          # 依赖管理 | Dependency management
│   ├── base.txt           # 基础依赖 | Base dependencies
│   └── dev.txt            # 开发依赖 | Development dependencies
├── tools/                 # 开发工具脚本 | Development tool scripts
│   ├── generate_changelog.py  # 自动生成更新日志 | Automatic changelog generation
│   ├── version-bump           # 版本升级工具 | Version upgrade tool
│   ├── pre-commit             # Git提交前钩子 | Git pre-commit hook
│   └── commit-msg             # Git提交消息验证钩子 | Git commit message verification hook
├── CHANGELOG.md           # 更新日志 | Changelog
└── README.md              # 项目说明文档 | Project documentation
```

## 安装方法 | Installation

这个项目使用现代Python打包方式和uv依赖管理。

This project uses modern Python packaging and uv dependency management.

### 使用uv安装 | Installation with uv

```bash
# 安装uv (如果尚未安装) | Install uv (if not already installed)
pip install uv

# 从仓库克隆 | Clone from repository
git clone https://github.com/yourusername/plan-manager.git
cd plan-manager

# 创建并激活虚拟环境 | Create and activate virtual environment
uv venv

# 在开发模式下安装 | Install in development mode
uv pip install -e .

# 如果需要安装开发依赖 | If you need to install development dependencies
uv pip install -r requirements/dev.txt
```

### 直接安装 | Direct Installation

```bash
# 安装发布版本 | Install released version
uv pip install plan-manager

# 或从GitHub安装最新版本 | Or install the latest version from GitHub
uv pip install git+https://github.com/yourusername/plan-manager.git
```

## 使用方法 | Usage

### 启动方式 | Launch Methods

安装后，可以通过以下命令启动：

After installation, you can start with the following commands:

```bash
# 命令行模式 | Command line mode
plan-manager

# 图形界面模式 | GUI mode
plan-manager-gui
# 或者 | or
plan-manager --gui
```

### 图形界面版本 | GUI Version

图形界面提供了直观的操作方式：
The graphical interface provides intuitive operation:

- 左侧面板可以筛选计划（按优先级、标签、完成状态）| Left panel for filtering plans (by priority, tag, completion status)
- 中间区域显示计划列表，不同优先级用不同颜色标注 | Middle area displays plan list, different priorities marked with different colors
- 右键点击计划可以进行快捷操作 | Right-click on plans for quick operations
- 双击计划可以查看详细信息 | Double-click plans to view details
- 顶部菜单和底部按钮提供各种功能 | Top menu and bottom buttons provide various functions

### 命令行版本 | Command Line Version

#### 基本命令 | Basic Commands

```bash
# 添加新计划 | Add new plan
plan-manager add "Plan Title" "Plan Description" --deadline 2023-12-31 --priority high --tags work important

# 列出所有计划 | List all plans
plan-manager list

# 按标签筛选计划 | Filter plans by tag
plan-manager list --tags work

# 按优先级筛选计划 | Filter plans by priority
plan-manager list --priority high

# 只显示未完成的计划 | Show only uncompleted plans
plan-manager list --uncompleted

# 只显示已完成的计划 | Show only completed plans
plan-manager list --completed

# 更新计划 | Update plan
plan-manager update PLAN_ID --title "New Title" --description "New Description" --deadline 2024-01-15

# 删除计划 | Delete plan
plan-manager delete PLAN_ID

# 标记计划为已完成 | Mark plan as completed
plan-manager complete PLAN_ID

# 查看即将到期的计划（默认7天内）| View upcoming plans (default within 7 days)
plan-manager upcoming

# 查看10天内即将到期的计划 | View plans due within 10 days
plan-manager upcoming --days 10
```

#### 参数说明 | Parameter Description

##### 添加计划 (add) | Add Plan
- `title`: 计划标题 | Plan title
- `description`: 计划描述 | Plan description
- `--deadline`, `-d`: 截止日期，格式为 YYYY-MM-DD | Deadline, format YYYY-MM-DD
- `--priority`, `-p`: 优先级，可选 low/medium/high，默认为 medium | Priority, options: low/medium/high, default: medium
- `--tags`, `-t`: 标签列表，可添加多个标签 | Tag list, can add multiple tags

##### 列出计划 (list) | List Plans
- `--tags`, `-t`: 按标签筛选 | Filter by tags
- `--priority`, `-p`: 按优先级筛选 | Filter by priority
- `--completed`, `-c`: 只显示已完成的计划 | Show only completed plans
- `--uncompleted`, `-u`: 只显示未完成的计划 | Show only uncompleted plans

##### 更新计划 (update) | Update Plan
- `id`: 计划ID | Plan ID
- `--title`: 更新标题 | Update title
- `--description`: 更新描述 | Update description
- `--deadline`, `-d`: 更新截止日期 | Update deadline
- `--priority`, `-p`: 更新优先级 | Update priority
- `--tags`, `-t`: 更新标签 | Update tags

##### 删除计划 (delete) | Delete Plan
- `id`: 计划ID | Plan ID

##### 完成计划 (complete) | Complete Plan
- `id`: 计划ID | Plan ID

##### 即将到期 (upcoming) | Upcoming Plans
- `--days`, `-d`: 未来天数，默认为7天 | Future days, default: 7 days

## 数据存储 | Data Storage

所有计划数据存储在当前目录下的 `plans.json` 文件中。您可以备份此文件以保存您的计划数据。命令行版本和图形界面版本共享同一个数据文件。

All plan data is stored in the `plans.json` file in the current directory. You can back up this file to save your plan data. The command line version and graphical interface version share the same data file.

## 开发 | Development

### 使用uv设置开发环境 | Setting Up Development Environment with uv

```bash
# 克隆仓库 | Clone repository
git clone https://github.com/yourusername/plan-manager.git
cd plan-manager

# 创建虚拟环境并安装开发依赖 | Create virtual environment and install development dependencies
uv venv
uv pip install -e ".[dev]"
# 或者 | or
uv pip install -r requirements/dev.txt

# 安装pre-commit钩子（推荐）| Install pre-commit hooks (recommended)
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
```

### 自动化工具 | Automation Tools

项目包含多个自动化工具，简化开发流程：
The project includes multiple automation tools to simplify the development process:

```bash
# 运行所有pre-commit检查 | Run all pre-commit checks
pre-commit run --all-files

# 代码格式化 | Code formatting
black plan_manager

# 类型检查 | Type checking
mypy plan_manager

# 代码风格检查 | Code style checking
flake8 plan_manager

# 自动生成更新日志（基于Git提交记录）| Automatically generate changelog (based on Git commit records)
python tools/generate_changelog.py

# 版本升级（自动更新版本号并生成更新日志）| Version upgrade (automatically update version number and generate changelog)
python tools/version-bump.py [major|minor|patch]
```

### Git提交规范 | Git Commit Convention

项目使用[约定式提交](https://www.conventionalcommits.org/zh-hans/)规范，提交消息格式为：
The project uses the [Conventional Commits](https://www.conventionalcommits.org/en/) specification, with the commit message format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

常用的类型包括：
Common types include:
- `feat`: 新功能 | New feature
- `fix`: 修复bug | Bug fix
- `docs`: 文档变更 | Documentation changes
- `style`: 代码风格变更 | Code style changes
- `refactor`: 代码重构 | Code refactoring
- `perf`: 性能优化 | Performance optimization
- `test`: 测试相关 | Test related
- `build`: 构建系统 | Build system
- `ci`: CI配置 | CI configuration
- `chore`: 其他杂项 | Other miscellaneous items

使用规范的提交消息可以自动生成结构化的更新日志。
Using standardized commit messages can automatically generate structured changelogs.

### 运行测试 | Running Tests

```bash
# 运行测试 | Run tests
uv pip run pytest

# 带覆盖率报告 | With coverage report
uv pip run pytest --cov=plan_manager
```

## 许可证 | License

AGPL-3.0 license
