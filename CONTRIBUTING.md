## 设置Git Hooks

请在克隆此仓库后运行以下命令设置Git钩子：

```bash
# 确保钩子脚本可执行
chmod +x tools/pre-commit tools/commit-msg tools/generate_changelog.py tools/version-bump

# 创建符号链接到.git/hooks目录
ln -sf ../../tools/pre-commit .git/hooks/pre-commit
ln -sf ../../tools/commit-msg .git/hooks/commit-msg
```
