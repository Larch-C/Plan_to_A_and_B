#!/usr/bin/env python3
# plan_manager.py - 计划储存自动化程序

import os
import json
import uuid
import datetime
import argparse
from typing import Dict, List, Optional, Any


class PlanManager:
    def __init__(self, storage_path: str = "plans.json"):
        self.storage_path = storage_path
        self.plans = self._load_plans()

    def _load_plans(self) -> Dict:
        """从存储文件加载计划"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"警告：计划文件 {self.storage_path} 损坏，创建新文件")
                return {"plans": []}
        return {"plans": []}

    def _save_plans(self) -> None:
        """保存计划到存储文件"""
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(self.plans, f, indent=4, ensure_ascii=False)

    def add_plan(
        self,
        title: str,
        description: str,
        deadline: Optional[str] = None,
        priority: str = "medium",
        tags: List[str] = None,
    ) -> str:
        """
        添加新计划

        参数:
            title: 计划标题
            description: 计划描述
            deadline: 截止日期 (YYYY-MM-DD 格式)
            priority: 优先级 (low, medium, high)
            tags: 标签列表

        返回:
            新计划的ID
        """
        tags = tags or []
        plan_id = str(uuid.uuid4())

        # 验证日期格式
        if deadline:
            try:
                datetime.datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                raise ValueError("截止日期格式必须为 YYYY-MM-DD")

        # 验证优先级
        if priority not in ["low", "medium", "high"]:
            raise ValueError("优先级必须为 low, medium 或 high")

        new_plan = {
            "id": plan_id,
            "title": title,
            "description": description,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "deadline": deadline,
            "priority": priority,
            "tags": tags,
            "completed": False,
        }

        self.plans["plans"].append(new_plan)
        self._save_plans()
        return plan_id

    def delete_plan(self, plan_id: str) -> bool:
        """
        删除计划

        参数:
            plan_id: 计划ID

        返回:
            是否成功删除
        """
        for i, plan in enumerate(self.plans["plans"]):
            if plan["id"] == plan_id:
                del self.plans["plans"][i]
                self._save_plans()
                return True
        return False

    def update_plan(self, plan_id: str, **kwargs) -> bool:
        """
        更新计划

        参数:
            plan_id: 计划ID
            **kwargs: 要更新的字段

        返回:
            是否成功更新
        """
        for plan in self.plans["plans"]:
            if plan["id"] == plan_id:
                # 验证日期格式
                if "deadline" in kwargs and kwargs["deadline"]:
                    try:
                        datetime.datetime.strptime(kwargs["deadline"], "%Y-%m-%d")
                    except ValueError:
                        raise ValueError("截止日期格式必须为 YYYY-MM-DD")

                # 验证优先级
                if "priority" in kwargs and kwargs["priority"] not in [
                    "low",
                    "medium",
                    "high",
                ]:
                    raise ValueError("优先级必须为 low, medium 或 high")

                # 更新字段
                for key, value in kwargs.items():
                    if key in plan and key != "id" and key != "created_at":
                        plan[key] = value

                self._save_plans()
                return True
        return False

    def get_plans(
        self, tags: List[str] = None, priority: str = None, completed: bool = None
    ) -> List[Dict]:
        """
        获取符合条件的计划

        参数:
            tags: 标签过滤
            priority: 优先级过滤
            completed: 完成状态过滤

        返回:
            符合条件的计划列表
        """
        result = self.plans["plans"]

        if tags:
            result = [
                plan for plan in result if any(tag in plan["tags"] for tag in tags)
            ]

        if priority:
            result = [plan for plan in result if plan["priority"] == priority]

        if completed is not None:
            result = [plan for plan in result if plan["completed"] == completed]

        return result

    def get_upcoming_deadlines(self, days: int = 7) -> List[Dict]:
        """
        获取即将到期的计划

        参数:
            days: 未来天数

        返回:
            未来指定天数内到期的计划列表
        """
        today = datetime.datetime.now().date()
        future = today + datetime.datetime.timedelta(days=days)

        result = []
        for plan in self.plans["plans"]:
            if not plan["deadline"] or plan["completed"]:
                continue

            deadline = datetime.datetime.strptime(plan["deadline"], "%Y-%m-%d").date()
            if today <= deadline <= future:
                result.append(plan)

        return sorted(result, key=lambda x: x["deadline"])

    def complete_plan(self, plan_id: str) -> bool:
        """
        标记计划为已完成

        参数:
            plan_id: 计划ID

        返回:
            是否成功标记
        """
        return self.update_plan(plan_id, completed=True)


def format_plan(plan: Dict) -> str:
    """格式化输出单个计划"""
    priority_colors = {
        "high": "\033[91m",  # 红色
        "medium": "\033[93m",  # 黄色
        "low": "\033[92m",  # 绿色
    }

    reset = "\033[0m"
    color = priority_colors.get(plan["priority"], "")

    result = [
        f"{color}[{plan['priority'].upper()}]{reset} {plan['title']}",
        f"ID: {plan['id']}",
        f"描述: {plan['description']}",
    ]

    if plan["deadline"]:
        result.append(f"截止日期: {plan['deadline']}")

    result.append(f"标签: {', '.join(plan['tags']) if plan['tags'] else '无'}")
    result.append(f"状态: {'已完成' if plan['completed'] else '未完成'}")
    result.append(f"创建于: {plan['created_at']}")

    return "\n".join(result)


def main():
    """命令行界面"""
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

    args = parser.parse_args()
    manager = PlanManager()

    if args.command == "add":
        try:
            plan_id = manager.add_plan(
                args.title, args.description, args.deadline, args.priority, args.tags
            )
            print(f"计划已添加，ID: {plan_id}")
        except ValueError as e:
            print(f"错误: {e}")

    elif args.command == "list":
        completed = None
        if args.completed:
            completed = True
        elif args.uncompleted:
            completed = False

        plans = manager.get_plans(args.tags, args.priority, completed)
        if not plans:
            print("没有找到符合条件的计划")
        else:
            for i, plan in enumerate(plans):
                print(format_plan(plan))
                if i < len(plans) - 1:
                    print("-" * 40)
            print(f"共 {len(plans)} 个计划")

    elif args.command == "update":
        try:
            kwargs = {}
            if args.title:
                kwargs["title"] = args.title
            if args.description:
                kwargs["description"] = args.description
            if args.deadline:
                kwargs["deadline"] = args.deadline
            if args.priority:
                kwargs["priority"] = args.priority
            if args.tags:
                kwargs["tags"] = args.tags

            if not kwargs:
                print("错误: 至少需要指定一个要更新的字段")
            elif manager.update_plan(args.id, **kwargs):
                print("计划已更新")
            else:
                print(f"未找到ID为 {args.id} 的计划")
        except ValueError as e:
            print(f"错误: {e}")

    elif args.command == "delete":
        if manager.delete_plan(args.id):
            print("计划已删除")
        else:
            print(f"未找到ID为 {args.id} 的计划")

    elif args.command == "complete":
        if manager.complete_plan(args.id):
            print("计划已标记为完成")
        else:
            print(f"未找到ID为 {args.id} 的计划")

    elif args.command == "upcoming":
        plans = manager.get_upcoming_deadlines(args.days)
        if not plans:
            print(f"未来 {args.days} 天内没有到期的计划")
        else:
            for i, plan in enumerate(plans):
                print(format_plan(plan))
                if i < len(plans) - 1:
                    print("-" * 40)
            print(f"共 {len(plans)} 个即将到期的计划")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
