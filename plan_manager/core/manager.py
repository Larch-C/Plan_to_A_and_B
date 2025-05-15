"""
计划管理器 - 提供计划的增删改查功能
"""

import os
import json
import datetime
from typing import Dict, List, Optional, Any

from ..models.plan import Plan


class PlanManager:
    """计划管理器类"""
    
    def __init__(self, storage_path: str = "plans.json"):
        """
        初始化计划管理器
        
        参数:
            storage_path: 存储计划数据的文件路径
        """
        self.storage_path = storage_path
        self.plans_data = self._load_plans()
    
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
            json.dump(self.plans_data, f, indent=4, ensure_ascii=False)
    
    def add_plan(self, title: str, description: str, deadline: Optional[str] = None, 
                priority: str = "medium", tags: List[str] = None) -> str:
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
        # 创建新计划对象
        plan = Plan(title, description, deadline, priority, tags)
        
        # 将计划转换为字典并添加到数据中
        self.plans_data["plans"].append(plan.to_dict())
        
        # 保存到文件
        self._save_plans()
        
        return plan.id
    
    def delete_plan(self, plan_id: str) -> bool:
        """
        删除计划
        
        参数:
            plan_id: 计划ID
            
        返回:
            是否成功删除
        """
        for i, plan_dict in enumerate(self.plans_data["plans"]):
            if plan_dict["id"] == plan_id:
                del self.plans_data["plans"][i]
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
        for plan_dict in self.plans_data["plans"]:
            if plan_dict["id"] == plan_id:
                # 创建计划对象进行验证
                plan = Plan.from_dict(plan_dict)
                
                # 更新属性
                for key, value in kwargs.items():
                    if hasattr(plan, key) and key != "id" and key != "created_at":
                        setattr(plan, key, value)
                
                # 验证数据有效性
                plan.validate()
                
                # 更新字典并保存
                updated_dict = plan.to_dict()
                for key, value in updated_dict.items():
                    plan_dict[key] = value
                
                self._save_plans()
                return True
        return False
    
    def get_plans(self, tags: List[str] = None, priority: str = None, 
                 completed: bool = None) -> List[Dict]:
        """
        获取符合条件的计划
        
        参数:
            tags: 标签过滤
            priority: 优先级过滤
            completed: 完成状态过滤
            
        返回:
            符合条件的计划列表
        """
        result = self.plans_data["plans"]
        
        if tags:
            result = [plan for plan in result if any(tag in plan["tags"] for tag in tags)]
            
        if priority:
            result = [plan for plan in result if plan["priority"] == priority]
            
        if completed is not None:
            result = [plan for plan in result if plan["completed"] == completed]
            
        return result
    
    def get_plan_by_id(self, plan_id: str) -> Optional[Dict]:
        """
        通过ID获取计划
        
        参数:
            plan_id: 计划ID
            
        返回:
            计划字典，如果不存在则返回None
        """
        for plan in self.plans_data["plans"]:
            if plan["id"] == plan_id:
                return plan
        return None
    
    def get_upcoming_deadlines(self, days: int = 7) -> List[Dict]:
        """
        获取即将到期的计划
        
        参数:
            days: 未来天数
            
        返回:
            未来指定天数内到期的计划列表
        """
        today = datetime.datetime.now().date()
        future = today + datetime.timedelta(days=days)
        
        result = []
        for plan in self.plans_data["plans"]:
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
        
    @property
    def plans(self) -> List[Plan]:
        """返回所有计划对象列表"""
        return [Plan.from_dict(plan_dict) for plan_dict in self.plans_data["plans"]] 