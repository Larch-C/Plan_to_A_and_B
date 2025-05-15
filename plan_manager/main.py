#!/usr/bin/env python3
"""
计划管理工具 - 主程序入口

这个模块提供计划管理工具的主入口点，支持命令行和图形界面两种方式启动
"""

import sys
import argparse
from typing import List

from plan_manager.cli import main as cli_main
from plan_manager.gui import run_gui


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="计划管理工具 - 帮助你存储、管理和跟踪各种计划任务"
    )

    parser.add_argument(
        "--gui", "-g", action="store_true", help="启动图形界面模式 (默认为命令行模式)"
    )

    # 将未识别的参数保留，以便传递给子命令处理器
    args, unknown = parser.parse_known_args()
    args.unknown = unknown
    return args


def main(argv: List[str] = None) -> int:
    """主函数，作为程序入口点"""
    if argv is None:
        argv = sys.argv

    args = parse_args()

    if args.gui:
        # 启动图形界面
        run_gui()
    else:
        # 启动命令行界面
        # 传递剩余参数给命令行解析器
        sys.argv = [sys.argv[0]] + args.unknown
        cli_main()

    return 0


def main_gui(argv: List[str] = None) -> int:
    """图形界面入口函数"""
    if argv is None:
        argv = sys.argv

    # 添加--gui参数强制使用图形界面
    if "--gui" not in argv and "-g" not in argv:
        argv.append("--gui")

    return main(argv)


if __name__ == "__main__":
    sys.exit(main())
