# 计划管理工具 (Plan Manager)

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

## 项目结构

```
plan_manager/
├── plan_manager/          # 包目录
│   ├── __init__.py        # 包初始化文件
│   ├── main.py            # 主程序入口
│   ├── models/            # 数据模型
│   │   ├── __init__.py
│   │   └── plan.py        # 计划数据模型
│   ├── core/              # 核心功能
│   │   ├── __init__.py
│   │   └── manager.py     # 计划管理器
│   ├── cli/               # 命令行接口
│   │   ├── __init__.py
│   │   └── main.py        # 命令行入口
│   ├── gui/               # 图形界面
│   │   ├── __init__.py
│   │   └── app.py         # GUI应用
│   ├── utils/             # 工具函数
│   │   ├── __init__.py
│   │   └── formatters.py  # 格式化工具
│   └── bin/               # 可执行脚本
│       ├── plan-manager      # 命令行启动脚本
│       └── plan-manager-gui  # GUI启动脚本
├── pyproject.toml         # 项目配置文件
├── requirements/          # 依赖管理
│   ├── base.txt           # 基础依赖
│   └── dev.txt            # 开发依赖
├── tools/                 # 开发工具脚本
│   ├── generate_changelog.py  # 自动生成更新日志
│   ├── version-bump           # 版本升级工具
│   ├── pre-commit             # Git提交前钩子
│   └── commit-msg             # Git提交消息验证钩子
├── CHANGELOG.md           # 更新日志
└── README.md              # 项目说明文档
```

## 安装方法

这个项目使用现代Python打包方式和uv依赖管理。

### 使用uv安装

```bash
# 安装uv (如果尚未安装)
pip install uv

# 从仓库克隆
git clone https://github.com/yourusername/plan-manager.git
cd plan-manager

# 创建并激活虚拟环境
uv venv

# 在开发模式下安装
uv pip install -e .

# 如果需要安装开发依赖
uv pip install -r requirements/dev.txt
```

### 直接安装

```bash
# 安装发布版本
uv pip install plan-manager

# 或从GitHub安装最新版本
uv pip install git+https://github.com/yourusername/plan-manager.git
```

## 使用方法

### 启动方式

安装后，可以通过以下命令启动：

```bash
# 命令行模式
plan-manager

# 图形界面模式
plan-manager-gui
# 或者
plan-manager --gui
```

### 图形界面版本

图形界面提供了直观的操作方式：
- 左侧面板可以筛选计划（按优先级、标签、完成状态）
- 中间区域显示计划列表，不同优先级用不同颜色标注
- 右键点击计划可以进行快捷操作
- 双击计划可以查看详细信息
- 顶部菜单和底部按钮提供各种功能

### 命令行版本

#### 基本命令

```bash
# 添加新计划
plan-manager add "计划标题" "计划描述" --deadline 2023-12-31 --priority high --tags 工作 重要

# 列出所有计划
plan-manager list

# 按标签筛选计划
plan-manager list --tags 工作

# 按优先级筛选计划
plan-manager list --priority high

# 只显示未完成的计划
plan-manager list --uncompleted

# 只显示已完成的计划
plan-manager list --completed

# 更新计划
plan-manager update 计划ID --title "新标题" --description "新描述" --deadline 2024-01-15

# 删除计划
plan-manager delete 计划ID

# 标记计划为已完成
plan-manager complete 计划ID

# 查看即将到期的计划（默认7天内）
plan-manager upcoming

# 查看10天内即将到期的计划
plan-manager upcoming --days 10
```

#### 参数说明

##### 添加计划 (add)
- `title`: 计划标题
- `description`: 计划描述
- `--deadline`, `-d`: 截止日期，格式为 YYYY-MM-DD
- `--priority`, `-p`: 优先级，可选 low/medium/high，默认为 medium
- `--tags`, `-t`: 标签列表，可添加多个标签

##### 列出计划 (list)
- `--tags`, `-t`: 按标签筛选
- `--priority`, `-p`: 按优先级筛选
- `--completed`, `-c`: 只显示已完成的计划
- `--uncompleted`, `-u`: 只显示未完成的计划

##### 更新计划 (update)
- `id`: 计划ID
- `--title`: 更新标题
- `--description`: 更新描述
- `--deadline`, `-d`: 更新截止日期
- `--priority`, `-p`: 更新优先级
- `--tags`, `-t`: 更新标签

##### 删除计划 (delete)
- `id`: 计划ID

##### 完成计划 (complete)
- `id`: 计划ID

##### 即将到期 (upcoming)
- `--days`, `-d`: 未来天数，默认为7天

## 数据存储

所有计划数据存储在当前目录下的 `plans.json` 文件中。您可以备份此文件以保存您的计划数据。命令行版本和图形界面版本共享同一个数据文件。

## 开发

### 使用uv设置开发环境

```bash
# 克隆仓库
git clone https://github.com/yourusername/plan-manager.git
cd plan-manager

# 创建虚拟环境并安装开发依赖
uv venv
uv pip install -e ".[dev]"
# 或者
uv pip install -r requirements/dev.txt

# 设置Git钩子（可选，推荐）
chmod +x tools/pre-commit tools/commit-msg
ln -sf ../../tools/pre-commit .git/hooks/pre-commit
ln -sf ../../tools/commit-msg .git/hooks/commit-msg
```

### 自动化工具

项目包含多个自动化工具，简化开发流程：

```bash
# 代码格式化
uv pip run black plan_manager tests

# 类型检查
uv pip run mypy plan_manager

# 代码风格检查
uv pip run flake8 plan_manager

# 自动生成更新日志（基于Git提交记录）
python tools/generate_changelog.py

# 版本升级（自动更新版本号并生成更新日志）
python tools/version-bump.py [major|minor|patch]
```

### Git提交规范

项目使用[约定式提交](https://www.conventionalcommits.org/zh-hans/)规范，提交消息格式为：

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

常用的类型包括：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档变更
- `style`: 代码风格变更
- `refactor`: 代码重构
- `perf`: 性能优化
- `test`: 测试相关
- `build`: 构建系统
- `ci`: CI配置
- `chore`: 其他杂项

使用规范的提交消息可以自动生成结构化的更新日志。

### 运行测试

```bash
# 运行测试
uv pip run pytest

# 带覆盖率报告
uv pip run pytest --cov=plan_manager
```

## 许可证

AGPL-3.0 license