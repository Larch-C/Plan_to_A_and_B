"""
命令行入口 - 处理命令行参数和交互
"""

import argparse
from typing import List, Optional

from ..core.manager import PlanManager
from ..utils.formatters import format_plan_for_display


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="计划管理工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # 添加计划
    add_parser = subparsers.add_parser("add", help="添加新计划")
    add_parser.add_argument("title", help="计划标题")
    add_parser.add_argument("description", help="计划描述")
    add_parser.add_argument("--deadline", "-d", help="截止日期 (YYYY-MM-DD)")
    add_parser.add_argument(
        "--priority",
        "-p",
        default="medium",
        choices=["low", "medium", "high"],
        help="优先级",
    )
    add_parser.add_argument("--tags", "-t", nargs="+", help="标签列表")

    # 列出计划
    list_parser = subparsers.add_parser("list", help="列出计划")
    list_parser.add_argument("--tags", "-t", nargs="+", help="按标签筛选")
    list_parser.add_argument(
        "--priority", "-p", choices=["low", "medium", "high"], help="按优先级筛选"
    )
    list_parser.add_argument(
        "--completed", "-c", action="store_true", help="只显示已完成的计划"
    )
    list_parser.add_argument(
        "--uncompleted", "-u", action="store_true", help="只显示未完成的计划"
    )

    # 更新计划
    update_parser = subparsers.add_parser("update", help="更新计划")
    update_parser.add_argument("id", help="计划ID")
    update_parser.add_argument("--title", help="更新标题")
    update_parser.add_argument("--description", help="更新描述")
    update_parser.add_argument("--deadline", "-d", help="更新截止日期 (YYYY-MM-DD)")
    update_parser.add_argument(
        "--priority", "-p", choices=["low", "medium", "high"], help="更新优先级"
    )
    update_parser.add_argument("--tags", "-t", nargs="+", help="更新标签")

    # 删除计划
    delete_parser = subparsers.add_parser("delete", help="删除计划")
    delete_parser.add_argument("id", help="计划ID")

    # 完成计划
    complete_parser = subparsers.add_parser("complete", help="标记计划为已完成")
    complete_parser.add_argument("id", help="计划ID")

    # 即将到期
    upcoming_parser = subparsers.add_parser("upcoming", help="查看即将到期的计划")
    upcoming_parser.add_argument("--days", "-d", type=int, default=7, help="未来天数")

    return parser.parse_args()


def add_plan(
    manager: PlanManager,
    title: str,
    description: str,
    deadline: Optional[str],
    priority: str,
    tags: List[str],
) -> None:
    """添加计划处理函数"""
    try:
        plan_id = manager.add_plan(title, description, deadline, priority, tags)
        print(f"计划已添加，ID: {plan_id}")
    except ValueError as e:
        print(f"错误: {e}")


def list_plans(
    manager: PlanManager, tags: List[str], priority: str, completed: Optional[bool]
) -> None:
    """列出计划处理函数"""
    plans = manager.get_plans(tags, priority, completed)
    if not plans:
        print("没有找到符合条件的计划")
    else:
        for i, plan in enumerate(plans):
            print(format_plan_for_display(plan))
            if i < len(plans) - 1:
                print("-" * 40)
        print(f"共 {len(plans)} 个计划")


def update_plan(manager: PlanManager, plan_id: str, **kwargs) -> None:
    """更新计划处理函数"""
    try:
        if not kwargs:
            print("错误: 至少需要指定一个要更新的字段")
        elif manager.update_plan(plan_id, **kwargs):
            print("计划已更新")
        else:
            print(f"未找到ID为 {plan_id} 的计划")
    except ValueError as e:
        print(f"错误: {e}")


def delete_plan(manager: PlanManager, plan_id: str) -> None:
    """删除计划处理函数"""
    if manager.delete_plan(plan_id):
        print("计划已删除")
    else:
        print(f"未找到ID为 {plan_id} 的计划")


def complete_plan(manager: PlanManager, plan_id: str) -> None:
    """完成计划处理函数"""
    if manager.complete_plan(plan_id):
        print("计划已标记为完成")
    else:
        print(f"未找到ID为 {plan_id} 的计划")


def show_upcoming(manager: PlanManager, days: int) -> None:
    """显示即将到期的计划处理函数"""
    plans = manager.get_upcoming_deadlines(days)
    if not plans:
        print(f"未来 {days} 天内没有到期的计划")
    else:
        for i, plan in enumerate(plans):
            print(format_plan_for_display(plan))
            if i < len(plans) - 1:
                print("-" * 40)
        print(f"共 {len(plans)} 个即将到期的计划")


def main():
    """命令行主函数"""
    args = parse_args()
    manager = PlanManager()

    if args.command == "add":
        add_plan(
            manager,
            args.title,
            args.description,
            args.deadline,
            args.priority,
            args.tags,
        )
    elif args.command == "list":
        completed = None
        if args.completed:
            completed = True
        elif args.uncompleted:
            completed = False
        list_plans(manager, args.tags, args.priority, completed)
    elif args.command == "update":
        kwargs = {}
        if args.title:
            kwargs["title"] = args.title
        if args.description:
            kwargs["description"] = args.description
        if args.deadline is not None:  # 允许设置为空
            kwargs["deadline"] = args.deadline
        if args.priority:
            kwargs["priority"] = args.priority
        if args.tags:
            kwargs["tags"] = args.tags
        update_plan(manager, args.id, **kwargs)
    elif args.command == "delete":
        delete_plan(manager, args.id)
    elif args.command == "complete":
        complete_plan(manager, args.id)
    elif args.command == "upcoming":
        show_upcoming(manager, args.days)
    else:
        # 如果没有指定命令，显示帮助
        parser = argparse.ArgumentParser(description="计划管理工具")
        parser.print_help()


if __name__ == "__main__":
    main()
