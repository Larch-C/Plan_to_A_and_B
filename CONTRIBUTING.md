## 设置Git Hooks

请在克隆此仓库后运行以下命令设置Git钩子：

```bash
# 确保钩子脚本可执行
chmod +x tools/pre-commit tools/commit-msg tools/generate_changelog.py tools/version-bump

# 创建符号链接到.git/hooks目录
ln -sf ../../tools/pre-commit .git/hooks/pre-commit
ln -sf ../../tools/commit-msg .git/hooks/commit-msg
```
## 设置Git Hooks

请在克隆此仓库后运行以下命令设置Git钩子：

```bash
# 确保钩子脚本可执行
chmod +x tools/pre-commit tools/commit-msg tools/generate_changelog.py tools/version-bump

# 创建符号链接到.git/hooks目录
ln -sf ../../tools/pre-commit .git/hooks/pre-commit
ln -sf ../../tools/commit-msg .git/hooks/commit-msg
```
## 代码质量检查

本项目使用 pre-commit 进行代码质量检查。请按照以下步骤设置：

```bash
# 安装pre-commit
pip install pre-commit

# 安装git hooks
pre-commit install
pre-commit install --hook-type commit-msg
```

pre-commit将在每次提交前自动运行以下检查：

- black：代码格式化
- flake8：代码风格检查
- mypy：类型检查
- 约定式提交格式验证
