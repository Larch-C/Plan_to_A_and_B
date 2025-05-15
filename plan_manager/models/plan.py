"""
计划模型 - 定义计划数据结构
"""

import uuid
import datetime
from typing import List, Optional, Dict, Any


class Plan:
    """计划数据模型类"""

    def __init__(
        self,
        title: str,
        description: str,
        deadline: Optional[str] = None,
        priority: str = "medium",
        tags: List[str] = None,
        plan_id: str = None,
        created_at: str = None,
        completed: bool = False,
    ):
        """
        初始化计划对象

        参数:
            title: 计划标题
            description: 计划描述
            deadline: 截止日期 (YYYY-MM-DD 格式)
            priority: 优先级 (low, medium, high)
            tags: 标签列表
            plan_id: 计划ID（如果不提供则自动生成）
            created_at: 创建时间（如果不提供则使用当前时间）
            completed: 是否已完成
        """
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.tags = tags or []
        self.id = plan_id or str(uuid.uuid4())
        self.created_at = created_at or datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.completed = completed

        # 验证数据
        self.validate()

    def validate(self):
        """验证计划数据的有效性"""
        # 验证日期格式
        if self.deadline:
            try:
                datetime.datetime.strptime(self.deadline, "%Y-%m-%d")
            except ValueError:
                raise ValueError("截止日期格式必须为 YYYY-MM-DD")

        # 验证优先级
        if self.priority not in ["low", "medium", "high"]:
            raise ValueError("优先级必须为 low, medium 或 high")

    def to_dict(self) -> Dict[str, Any]:
        """将计划对象转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
            "deadline": self.deadline,
            "priority": self.priority,
            "tags": self.tags,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Plan":
        """从字典创建计划对象"""
        return cls(
            title=data["title"],
            description=data["description"],
            deadline=data.get("deadline"),
            priority=data.get("priority", "medium"),
            tags=data.get("tags", []),
            plan_id=data.get("id"),
            created_at=data.get("created_at"),
            completed=data.get("completed", False),
        )

    def __str__(self) -> str:
        """返回计划的字符串表示"""
        status = "已完成" if self.completed else "未完成"
        deadline = f"截止日期: {self.deadline}" if self.deadline else "无截止日期"
        tags = f"标签: {', '.join(self.tags)}" if self.tags else "无标签"

        return (
            f"{self.title} [{self.priority.upper()}] ({status})\n"
            f"ID: {self.id}\n"
            f"描述: {self.description}\n"
            f"{deadline}\n"
            f"{tags}\n"
            f"创建于: {self.created_at}"
        )
