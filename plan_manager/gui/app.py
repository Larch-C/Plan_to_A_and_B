"""
GUI应用 - 提供图形界面交互
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List, Optional, Any

from ..core.manager import PlanManager
from ..utils.formatters import get_priority_display_name, get_priority_display_color


class PlanManagerGUI:
    """计划管理器图形界面类"""

    def __init__(self, root):
        """初始化图形界面"""
        self.root = root
        self.root.title("计划管理工具")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)

        # 设置主题颜色
        self.bg_color = "#f5f5f5"
        self.accent_color = "#4a6baf"
        self.root.configure(bg=self.bg_color)

        # 初始化计划管理器
        self.plan_manager = PlanManager()
        self.current_filter = {"tags": None, "priority": None, "completed": None}

        self.setup_styles()
        self.create_menu()
        self.create_widgets()
        self.load_plans()

        # 设置窗口图标
        try:
            self.root.iconbitmap("icon.ico")  # 如果有图标文件的话
        except:
            pass

    def setup_styles(self):
        """设置自定义样式"""
        style = ttk.Style()
        style.theme_use("clam")  # 使用clam主题作为基础

        # 配置Treeview样式
        style.configure(
            "Treeview",
            background=self.bg_color,
            fieldbackground=self.bg_color,
            foreground="black",
            rowheight=30,
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold"),
            background=self.accent_color,
            foreground="white",
        )

        # 按钮样式
        style.configure(
            "Accent.TButton", background=self.accent_color, foreground="white"
        )

        # 标签样式
        style.configure("TLabel", background=self.bg_color, font=("Arial", 10))

        # 框架样式
        style.configure("TFrame", background=self.bg_color)

        # 选项卡样式
        style.configure("TNotebook", background=self.bg_color)
        style.configure("TNotebook.Tab", padding=[10, 5], font=("Arial", 10))

    def create_menu(self):
        """创建菜单栏"""
        menu_bar = tk.Menu(self.root)

        # 文件菜单
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="导出数据", command=self.export_data)
        file_menu.add_command(label="导入数据", command=self.import_data)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menu_bar.add_cascade(label="文件", menu=file_menu)

        # 编辑菜单
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="添加计划", command=self.show_add_plan_dialog)
        edit_menu.add_command(label="清除筛选", command=self.clear_filters)
        menu_bar.add_cascade(label="编辑", menu=edit_menu)

        # 查看菜单
        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="刷新", command=self.load_plans)
        view_menu.add_command(
            label="只显示未完成", command=lambda: self.filter_by_completion(False)
        )
        view_menu.add_command(
            label="只显示已完成", command=lambda: self.filter_by_completion(True)
        )
        view_menu.add_command(label="即将到期", command=self.show_upcoming)
        menu_bar.add_cascade(label="查看", menu=view_menu)

        # 帮助菜单
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="使用帮助", command=self.show_help)
        help_menu.add_command(label="关于", command=self.show_about)
        menu_bar.add_cascade(label="帮助", menu=help_menu)

        self.root.config(menu=menu_bar)

    def create_widgets(self):
        """创建主界面组件"""
        # 主分割窗口
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧筛选面板
        self.filter_frame = ttk.Frame(self.main_paned, style="TFrame", width=200)

        # 右侧内容区
        self.content_frame = ttk.Frame(self.main_paned, style="TFrame")

        self.main_paned.add(self.filter_frame, weight=1)
        self.main_paned.add(self.content_frame, weight=4)

        # 创建筛选控件
        self.create_filter_widgets()

        # 创建计划列表
        self.create_plan_list()

        # 创建操作按钮
        self.create_action_buttons()

    def create_filter_widgets(self):
        """创建筛选面板组件"""
        ttk.Label(self.filter_frame, text="筛选", font=("Arial", 12, "bold")).pack(
            pady=(0, 10), anchor=tk.W
        )

        # 优先级筛选
        ttk.Label(self.filter_frame, text="优先级:").pack(pady=(10, 5), anchor=tk.W)

        self.priority_var = tk.StringVar()
        priority_frame = ttk.Frame(self.filter_frame)
        priority_frame.pack(fill=tk.X, pady=5)

        priorities = [("全部", ""), ("低", "low"), ("中", "medium"), ("高", "high")]
        for text, value in priorities:
            ttk.Radiobutton(
                priority_frame,
                text=text,
                value=value,
                variable=self.priority_var,
                command=self.apply_filters,
            ).pack(side=tk.LEFT, padx=5)

        # 完成状态筛选
        ttk.Label(self.filter_frame, text="完成状态:").pack(pady=(10, 5), anchor=tk.W)

        self.completion_var = tk.StringVar(value="all")
        completion_frame = ttk.Frame(self.filter_frame)
        completion_frame.pack(fill=tk.X, pady=5)

        completions = [
            ("全部", "all"),
            ("未完成", "uncompleted"),
            ("已完成", "completed"),
        ]
        for text, value in completions:
            ttk.Radiobutton(
                completion_frame,
                text=text,
                value=value,
                variable=self.completion_var,
                command=self.apply_filters,
            ).pack(side=tk.LEFT, padx=5)

        # 标签筛选
        ttk.Label(self.filter_frame, text="标签:").pack(pady=(10, 5), anchor=tk.W)

        self.tags_entry = ttk.Entry(self.filter_frame)
        self.tags_entry.pack(fill=tk.X, pady=5)

        ttk.Button(
            self.filter_frame, text="应用标签筛选", command=self.apply_tag_filter
        ).pack(pady=5, anchor=tk.W)

        # 分隔线
        ttk.Separator(self.filter_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        # 清除所有筛选按钮
        ttk.Button(
            self.filter_frame, text="清除所有筛选", command=self.clear_filters
        ).pack(pady=10, anchor=tk.W)

        # 即将到期筛选
        ttk.Button(
            self.filter_frame, text="查看即将到期", command=self.show_upcoming
        ).pack(pady=5, anchor=tk.W)

    def create_plan_list(self):
        """创建计划列表区域"""
        # 列表上方的标题和搜索框
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(header_frame, text="计划列表", font=("Arial", 14, "bold")).pack(
            side=tk.LEFT
        )

        # 计划列表（使用Treeview）
        columns = ("id", "title", "priority", "deadline", "tags", "status")
        self.plan_tree = ttk.Treeview(
            self.content_frame, columns=columns, show="headings", style="Treeview"
        )

        # 设置列标题
        self.plan_tree.heading("id", text="ID")
        self.plan_tree.heading("title", text="标题")
        self.plan_tree.heading("priority", text="优先级")
        self.plan_tree.heading("deadline", text="截止日期")
        self.plan_tree.heading("tags", text="标签")
        self.plan_tree.heading("status", text="状态")

        # 设置列宽
        self.plan_tree.column("id", width=50)
        self.plan_tree.column("title", width=200)
        self.plan_tree.column("priority", width=80)
        self.plan_tree.column("deadline", width=100)
        self.plan_tree.column("tags", width=150)
        self.plan_tree.column("status", width=80)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(
            self.content_frame, orient=tk.VERTICAL, command=self.plan_tree.yview
        )
        self.plan_tree.configure(yscrollcommand=scrollbar.set)

        # 双击事件绑定
        self.plan_tree.bind("<Double-1>", self.on_plan_double_click)
        # 右键菜单绑定
        self.plan_tree.bind("<Button-3>", self.show_context_menu)

        # 布局
        self.plan_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建右键菜单
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="查看详情", command=self.view_plan_details)
        self.context_menu.add_command(label="编辑计划", command=self.edit_selected_plan)
        self.context_menu.add_command(
            label="删除计划", command=self.delete_selected_plan
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label="标记为已完成", command=self.complete_selected_plan
        )

    def create_action_buttons(self):
        """创建底部操作按钮"""
        button_frame = ttk.Frame(self.content_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            button_frame,
            text="添加计划",
            style="Accent.TButton",
            command=self.show_add_plan_dialog,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="编辑计划", command=self.edit_selected_plan).pack(
            side=tk.LEFT, padx=5
        )

        ttk.Button(
            button_frame, text="删除计划", command=self.delete_selected_plan
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame, text="标记完成", command=self.complete_selected_plan
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="查看详情", command=self.view_plan_details).pack(
            side=tk.LEFT, padx=5
        )

        ttk.Button(button_frame, text="刷新", command=self.load_plans).pack(
            side=tk.RIGHT, padx=5
        )

    def load_plans(self):
        """加载计划到列表视图"""
        # 清空现有列表
        for item in self.plan_tree.get_children():
            self.plan_tree.delete(item)

        # 根据筛选条件获取计划
        tags = None
        if self.current_filter["tags"]:
            tags = self.current_filter["tags"]

        priority = self.current_filter["priority"]

        completed = self.current_filter["completed"]

        # 从计划管理器获取过滤后的计划
        plans = self.plan_manager.get_plans(tags, priority, completed)

        # 按截止日期排序
        if plans:
            # 未设置截止日期的计划放在最后
            def sort_key(plan):
                if not plan["deadline"]:
                    return "9999-99-99"  # 一个很大的日期值
                return plan["deadline"]

            plans.sort(key=sort_key)

        # 添加到树状视图
        for plan in plans:
            # 格式化显示内容
            plan_id = plan["id"][:8]  # 只显示ID的前8位
            title = plan["title"]
            priority = get_priority_display_name(plan["priority"])
            deadline = plan["deadline"] if plan["deadline"] else "无"
            tags = ", ".join(plan["tags"]) if plan["tags"] else "无"
            status = "已完成" if plan["completed"] else "未完成"

            # 根据优先级和状态决定标签颜色
            if plan["completed"]:
                tag = "completed"
            else:
                tag = plan["priority"]

            item_id = self.plan_tree.insert(
                "",
                tk.END,
                values=(plan_id, title, priority, deadline, tags, status),
                tags=(tag,),
            )

            # 将完整的计划ID存储为项目的属性
            self.plan_tree.item(item_id, tags=(tag, plan["id"]))

        # 设置行颜色
        self.plan_tree.tag_configure("high", background="#ffcccc")
        self.plan_tree.tag_configure("medium", background="#ffffcc")
        self.plan_tree.tag_configure("low", background="#ccffcc")
        self.plan_tree.tag_configure(
            "completed", background="#e0e0e0", foreground="#888888"
        )

    def apply_filters(self):
        """应用优先级和完成状态筛选"""
        priority = self.priority_var.get() if self.priority_var.get() else None

        completion = self.completion_var.get()
        if completion == "completed":
            completed = True
        elif completion == "uncompleted":
            completed = False
        else:
            completed = None

        self.current_filter["priority"] = priority
        self.current_filter["completed"] = completed

        self.load_plans()

    def apply_tag_filter(self):
        """应用标签筛选"""
        tags_text = self.tags_entry.get().strip()
        if tags_text:
            tags = [tag.strip() for tag in tags_text.split(",")]
            self.current_filter["tags"] = tags
        else:
            self.current_filter["tags"] = None

        self.load_plans()

    def clear_filters(self):
        """清除所有筛选条件"""
        self.current_filter = {"tags": None, "priority": None, "completed": None}
        self.priority_var.set("")
        self.completion_var.set("all")
        self.tags_entry.delete(0, tk.END)

        self.load_plans()

    def filter_by_completion(self, completed):
        """按完成状态筛选"""
        self.current_filter["completed"] = completed
        self.completion_var.set("completed" if completed else "uncompleted")
        self.load_plans()

    def show_upcoming(self):
        """显示即将到期的计划"""
        days = simpledialog.askinteger(
            "即将到期", "请输入天数:", initialvalue=7, minvalue=1, maxvalue=365
        )
        if days is None:
            return

        # 清空现有列表
        for item in self.plan_tree.get_children():
            self.plan_tree.delete(item)

        # 获取即将到期的计划
        plans = self.plan_manager.get_upcoming_deadlines(days)

        # 添加到树状视图
        for plan in plans:
            plan_id = plan["id"][:8]
            title = plan["title"]
            priority = get_priority_display_name(plan["priority"])
            deadline = plan["deadline"]
            tags = ", ".join(plan["tags"]) if plan["tags"] else "无"
            status = "已完成" if plan["completed"] else "未完成"

            # 根据优先级决定标签颜色
            tag = plan["priority"]

            item_id = self.plan_tree.insert(
                "",
                tk.END,
                values=(plan_id, title, priority, deadline, tags, status),
                tags=(tag,),
            )
            self.plan_tree.item(item_id, tags=(tag, plan["id"]))

        # 显示过滤提示
        if plans:
            messagebox.showinfo(
                "即将到期", f"显示未来 {days} 天内即将到期的 {len(plans)} 个计划"
            )
        else:
            messagebox.showinfo("即将到期", f"未来 {days} 天内没有即将到期的计划")

    def get_selected_plan_id(self):
        """获取当前选中计划的完整ID"""
        selection = self.plan_tree.selection()
        if not selection:
            messagebox.showinfo("提示", "请先选择一个计划")
            return None

        item = self.plan_tree.item(selection[0])
        tags = item["tags"]

        # 获取完整的计划ID（存储在tag中的第二个元素）
        if len(tags) >= 2:
            return tags[1]

        return None

    def view_plan_details(self):
        """查看计划详情"""
        plan_id = self.get_selected_plan_id()
        if not plan_id:
            return

        # 获取计划详情
        plan_dict = self.plan_manager.get_plan_by_id(plan_id)
        if not plan_dict:
            messagebox.showerror("错误", "找不到该计划")
            return

        # 创建详情对话框
        details_window = tk.Toplevel(self.root)
        details_window.title("计划详情")
        details_window.geometry("500x400")
        details_window.resizable(False, False)
        details_window.configure(bg=self.bg_color)

        # 详情内容
        main_frame = ttk.Frame(details_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 标题
        ttk.Label(main_frame, text=plan_dict["title"], font=("Arial", 16, "bold")).pack(
            anchor=tk.W, pady=(0, 10)
        )

        # 优先级标签
        priority_frame = ttk.Frame(main_frame)
        priority_frame.pack(fill=tk.X, pady=5)

        priority_colors = {"high": "#ff6666", "medium": "#ffcc66", "low": "#66cc66"}
        priority_label = ttk.Label(priority_frame, text=f"优先级: ", font=("Arial", 10))
        priority_label.pack(side=tk.LEFT)

        priority_value = tk.Label(
            priority_frame,
            text=plan_dict["priority"].upper(),
            bg=priority_colors.get(plan_dict["priority"], self.bg_color),
            font=("Arial", 10, "bold"),
        )
        priority_value.pack(side=tk.LEFT, padx=5)

        # 描述
        desc_frame = ttk.LabelFrame(main_frame, text="描述")
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        desc_text = tk.Text(desc_frame, wrap=tk.WORD, height=5, font=("Arial", 10))
        desc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        desc_text.insert(tk.END, plan_dict["description"])
        desc_text.configure(state="disabled")

        # 其他信息
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=10)

        # 左侧信息
        left_frame = ttk.Frame(info_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        if plan_dict["deadline"]:
            ttk.Label(
                left_frame,
                text=f"截止日期: {plan_dict['deadline']}",
                font=("Arial", 10),
            ).pack(anchor=tk.W, pady=2)
        else:
            ttk.Label(left_frame, text="截止日期: 无", font=("Arial", 10)).pack(
                anchor=tk.W, pady=2
            )

        ttk.Label(
            left_frame, text=f"创建于: {plan_dict['created_at']}", font=("Arial", 10)
        ).pack(anchor=tk.W, pady=2)

        # 右侧信息
        right_frame = ttk.Frame(info_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        status_text = "已完成" if plan_dict["completed"] else "未完成"
        ttk.Label(right_frame, text=f"状态: {status_text}", font=("Arial", 10)).pack(
            anchor=tk.W, pady=2
        )

        tags_text = ", ".join(plan_dict["tags"]) if plan_dict["tags"] else "无"
        ttk.Label(right_frame, text=f"标签: {tags_text}", font=("Arial", 10)).pack(
            anchor=tk.W, pady=2
        )

        # 底部按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            button_frame,
            text="编辑",
            command=lambda: [details_window.destroy(), self.edit_selected_plan()],
        ).pack(side=tk.LEFT, padx=5)

        if not plan_dict["completed"]:
            ttk.Button(
                button_frame,
                text="标记为已完成",
                command=lambda: [details_window.destroy(), self.complete_plan(plan_id)],
            ).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="关闭", command=details_window.destroy).pack(
            side=tk.RIGHT, padx=5
        )

    def show_add_plan_dialog(self):
        """显示添加计划对话框"""
        self.show_plan_dialog()

    def show_plan_dialog(self, plan_id=None):
        """显示计划编辑/添加对话框"""
        # 如果是编辑现有计划，则获取计划信息
        plan_dict = None
        if plan_id:
            plan_dict = self.plan_manager.get_plan_by_id(plan_id)

            if not plan_dict:
                messagebox.showerror("错误", "找不到该计划")
                return

        # 创建对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("添加计划" if not plan_dict else "编辑计划")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        dialog.configure(bg=self.bg_color)
        dialog.grab_set()  # 模态对话框

        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 标题输入
        ttk.Label(main_frame, text="标题:").pack(anchor=tk.W, pady=(0, 5))
        title_var = tk.StringVar(value=plan_dict["title"] if plan_dict else "")
        title_entry = ttk.Entry(main_frame, textvariable=title_var, width=50)
        title_entry.pack(fill=tk.X, pady=(0, 10))

        # 描述输入
        ttk.Label(main_frame, text="描述:").pack(anchor=tk.W, pady=(0, 5))
        desc_text = tk.Text(main_frame, wrap=tk.WORD, height=5)
        desc_text.pack(fill=tk.X, pady=(0, 10))
        if plan_dict:
            desc_text.insert(tk.END, plan_dict["description"])

        # 截止日期
        ttk.Label(main_frame, text="截止日期 (YYYY-MM-DD):").pack(
            anchor=tk.W, pady=(0, 5)
        )
        deadline_var = tk.StringVar(
            value=plan_dict["deadline"] if plan_dict and plan_dict["deadline"] else ""
        )
        deadline_entry = ttk.Entry(main_frame, textvariable=deadline_var)
        deadline_entry.pack(fill=tk.X, pady=(0, 10))

        # 优先级
        ttk.Label(main_frame, text="优先级:").pack(anchor=tk.W, pady=(0, 5))
        priority_var = tk.StringVar(
            value=plan_dict["priority"] if plan_dict else "medium"
        )
        priority_frame = ttk.Frame(main_frame)
        priority_frame.pack(fill=tk.X, pady=(0, 10))

        priorities = [("低", "low"), ("中", "medium"), ("高", "high")]
        for text, value in priorities:
            ttk.Radiobutton(
                priority_frame, text=text, value=value, variable=priority_var
            ).pack(side=tk.LEFT, padx=10)

        # 标签
        ttk.Label(main_frame, text="标签 (用逗号分隔):").pack(anchor=tk.W, pady=(0, 5))
        tags_var = tk.StringVar(
            value=(
                ", ".join(plan_dict["tags"]) if plan_dict and plan_dict["tags"] else ""
            )
        )
        tags_entry = ttk.Entry(main_frame, textvariable=tags_var)
        tags_entry.pack(fill=tk.X, pady=(0, 10))

        # 完成状态
        status_var = tk.BooleanVar(value=plan_dict["completed"] if plan_dict else False)
        status_check = ttk.Checkbutton(main_frame, text="已完成", variable=status_var)
        status_check.pack(anchor=tk.W, pady=(0, 20))

        # 按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        def save_plan():
            # 获取输入值
            title = title_var.get().strip()
            description = desc_text.get("1.0", tk.END).strip()
            deadline = deadline_var.get().strip()
            priority = priority_var.get()
            tags_text = tags_var.get().strip()
            completed = status_var.get()

            if not title:
                messagebox.showerror("错误", "标题不能为空")
                return

            # 解析标签
            tags = [tag.strip() for tag in tags_text.split(",")] if tags_text else []

            try:
                if plan_dict:
                    # 更新现有计划
                    self.plan_manager.update_plan(
                        plan_id,
                        title=title,
                        description=description,
                        deadline=deadline if deadline else None,
                        priority=priority,
                        tags=tags,
                        completed=completed,
                    )
                    messagebox.showinfo("成功", "计划已更新")
                else:
                    # 添加新计划
                    new_id = self.plan_manager.add_plan(
                        title,
                        description,
                        deadline if deadline else None,
                        priority,
                        tags,
                    )
                    if completed:
                        self.plan_manager.complete_plan(new_id)
                    messagebox.showinfo("成功", "计划已添加")

                dialog.destroy()
                self.load_plans()

            except ValueError as e:
                messagebox.showerror("错误", str(e))

        ttk.Button(
            button_frame, text="保存", command=save_plan, style="Accent.TButton"
        ).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(
            side=tk.RIGHT, padx=5
        )

        # 设置初始焦点
        title_entry.focus_set()

    def edit_selected_plan(self):
        """编辑选中的计划"""
        plan_id = self.get_selected_plan_id()
        if plan_id:
            self.show_plan_dialog(plan_id)

    def delete_selected_plan(self):
        """删除选中的计划"""
        plan_id = self.get_selected_plan_id()
        if not plan_id:
            return

        # 确认删除
        confirm = messagebox.askyesno(
            "确认删除", "确定要删除这个计划吗？此操作不可恢复。"
        )
        if not confirm:
            return

        # 执行删除
        success = self.plan_manager.delete_plan(plan_id)
        if success:
            messagebox.showinfo("成功", "计划已删除")
            self.load_plans()
        else:
            messagebox.showerror("错误", "删除计划失败")

    def complete_selected_plan(self):
        """将选中的计划标记为已完成"""
        plan_id = self.get_selected_plan_id()
        if plan_id:
            self.complete_plan(plan_id)

    def complete_plan(self, plan_id):
        """标记计划为已完成"""
        success = self.plan_manager.complete_plan(plan_id)
        if success:
            messagebox.showinfo("成功", "计划已标记为完成")
            self.load_plans()
        else:
            messagebox.showerror("错误", "操作失败")

    def on_plan_double_click(self, event):
        """处理计划项双击事件"""
        self.view_plan_details()

    def show_context_menu(self, event):
        """显示右键菜单"""
        # 先选择点击的项
        item = self.plan_tree.identify_row(event.y)
        if item:
            self.plan_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def export_data(self):
        """导出计划数据"""
        messagebox.showinfo(
            "导出数据", f"数据已保存到 {self.plan_manager.storage_path}"
        )

    def import_data(self):
        """导入计划数据功能待开发"""
        messagebox.showinfo("导入数据", "此功能正在开发中")

    def show_help(self):
        """显示帮助信息"""
        help_text = """
        计划管理工具使用指南：

        1. 添加计划：点击"添加计划"按钮或使用编辑菜单。
        2. 编辑计划：选中计划后点击"编辑计划"或双击计划项。
        3. 删除计划：选中计划后点击"删除计划"或右键菜单选择删除。
        4. 标记完成：选中计划后点击"标记完成"按钮。
        5. 筛选计划：使用左侧筛选面板按不同条件筛选。
        6. 查看即将到期：点击左侧"查看即将到期"按钮。
        7. 数据存储：所有数据保存在plans.json文件中。
        """

        help_window = tk.Toplevel(self.root)
        help_window.title("使用帮助")
        help_window.geometry("600x400")
        help_window.configure(bg=self.bg_color)

        text = tk.Text(help_window, wrap=tk.WORD, padx=20, pady=20)
        text.pack(fill=tk.BOTH, expand=True)
        text.insert(tk.END, help_text)
        text.configure(state="disabled")

    def show_about(self):
        """显示关于信息"""
        about_text = """
        计划管理工具 (Plan Manager GUI)

        版本: 1.0.0

        这是一个简单的计划管理工具，帮助您轻松管理和跟踪各种计划任务。

        功能包括:
        - 添加、编辑、删除计划
        - 设置优先级和截止日期
        - 标记计划完成状态
        - 筛选和查看计划
        - 查看即将到期的计划
        """

        messagebox.showinfo("关于", about_text)


def run_gui():
    """启动GUI应用"""
    root = tk.Tk()
    app = PlanManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
