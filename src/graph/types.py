# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT


from langgraph.graph import MessagesState

from src.prompts.planner_model import Plan
from src.rag import Resource


class State(MessagesState):
    """State for the agent system, extends MessagesState with next field."""

    # Runtime Variables
    locale: str = "en-US"
    research_topic: str = ""  # 用户输入提示词
    observations: list[str] = []
    resources: list[Resource] = []
    plan_iterations: int = 0  # 计划迭代次数
    format_retry_count: int  # JSON格式错误重试计数器
    current_plan: Plan | str = None
    final_report: str = ""
    auto_accepted_plan: bool = False
    enable_background_investigation: bool = True
    background_investigation_results: str = None
    # todo
    tools_description: str=""  # 工具的描述信息
    few_shots: str=""  # 工具调用示例
