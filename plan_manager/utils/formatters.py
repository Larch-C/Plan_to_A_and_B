"""
格式化工具 - 提供格式化输出计划的工具函数
"""

from typing import Dict, Any


def format_plan_color(priority: str) -> str:
    """
    根据优先级返回控制台颜色代码
    
    参数:
        priority: 优先级 (low, medium, high)
        
    返回:
        ANSI颜色代码
    """
    priority_colors = {
        "high": "\033[91m",  # 红色
        "medium": "\033[93m",  # 黄色
        "low": "\033[92m",  # 绿色
    }
    return priority_colors.get(priority, "")


def format_plan_for_display(plan: Dict[str, Any]) -> str:
    """
    格式化输出单个计划，适用于命令行显示
    
    参数:
        plan: 计划字典
        
    返回:
        格式化后的字符串
    """
    reset = "\033[0m"
    color = format_plan_color(plan["priority"])
    
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


def get_priority_display_name(priority: str) -> str:
    """
    获取优先级的显示名称
    
    参数:
        priority: 优先级 (low, medium, high)
        
    返回:
        中文显示名称
    """
    priority_map = {"low": "低", "medium": "中", "high": "高"}
    return priority_map.get(priority, priority)


def get_priority_display_color(priority: str) -> str:
    """
    获取优先级在GUI中显示的颜色
    
    参数:
        priority: 优先级 (low, medium, high)
        
    返回:
        十六进制颜色代码
    """
    priority_colors = {
        "high": "#ffcccc",  # 浅红色
        "medium": "#ffffcc",  # 浅黄色
        "low": "#ccffcc",  # 浅绿色
    }
    return priority_colors.get(priority, "#ffffff") 