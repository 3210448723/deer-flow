# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

# 导入LangGraph库中的核心组件
from langgraph.graph import StateGraph, START, END  # 状态图及其起始、结束节点
from langgraph.checkpoint.memory import MemorySaver  # 内存保存器，用于保存对话历史
from src.prompts.planner_model import StepType  # 导入步骤类型枚举

# 导入本地类型和节点函数
from .types import State  # 状态类，用于定义图的状态结构
from .nodes import (
    coordinator_node,      # 协调者节点：决定问题类型和处理流程
    planner_node,          # 规划者节点：制定解决问题的步骤
    reporter_node,         # 报告者节点：生成最终回答
    research_team_node,    # 研究团队节点：管理研究流程
    researcher_node,       # 研究员节点：执行研究步骤
    coder_node,            # 编码员节点：执行代码处理步骤
    human_feedback_node,   # 人类反馈节点：处理用户反馈
    background_investigation_node,  # 背景调查节点：执行联网搜索
)

# todo 如果多智能体要加这里要改
def continue_to_running_research_team(state: State):
    """
    条件路由函数：决定下一步执行哪个节点

    根据当前计划的执行状态，决定工作流程应该路由到哪个节点：
    - 如果没有计划或所有步骤已完成，返回规划者节点
    - 否则根据下一个未执行步骤的类型，选择适当的执行者节点

    参数:
        state: 当前的状态对象，包含当前计划信息

    返回:
        下一个要执行的节点名称（字符串）
    """
    current_plan = state.get("current_plan")
    # 如果没有计划或计划没有步骤，回到规划者节点
    if not current_plan or not current_plan.steps:
        return "planner"

    if all(step.execution_res for step in current_plan.steps):
        return "planner"

    # Find first incomplete step
    incomplete_step = None
    for step in current_plan.steps:
        if not step.execution_res:
            incomplete_step = step
            break

    if not incomplete_step:
        return "planner"

    if incomplete_step.step_type == StepType.RESEARCH:
        return "researcher"
    if incomplete_step.step_type == StepType.PROCESSING:
        return "coder"
    return "planner"


def _build_base_graph():
    """
    构建并返回基础状态图，包含所有节点和边

    这个函数创建了一个完整的工作流程图，定义了各种智能体节点和它们之间的连接关系，
    形成了一个多智能体协作系统的骨架结构。

    返回:
        构建好的但尚未编译的StateGraph对象
    """
    # 创建基于State类型的状态图
    builder = StateGraph(State)

    # 添加起始边，流程从coordinator节点开始
    builder.add_edge(START, "coordinator")

    # 添加各种节点，并指定其实现函数
    builder.add_node("coordinator", coordinator_node)  # 识别简单还是复杂问题的协调节点
    builder.add_node("background_investigator", background_investigation_node)  # 联网搜索节点
    builder.add_node("planner", planner_node)  # 规划智能体，负责制定解决问题的计划
    builder.add_node("reporter", reporter_node)  # 最终回答智能体，生成最终输出

    # 智能体组 - 负责执行不同类型的任务
    builder.add_node("research_team", research_team_node)  # 研究团队管理节点
    builder.add_node("researcher", researcher_node)  # 执行研究任务的节点
    builder.add_node("coder", coder_node)  # 执行代码处理任务的节点
    # Todo: 数据分析智能体、安全监控智能体 - 未来可能添加的节点

    # 添加人类反馈节点，用于处理用户输入
    builder.add_node("human_feedback", human_feedback_node)

    # 添加从背景调查到规划者的边，表示背景调查完成后进行规划
    builder.add_edge("background_investigator", "planner")

    # 添加条件边，研究团队节点完成后根据continue_to_running_research_team函数的返回值选择下一节点
    builder.add_conditional_edges(
        "research_team",
        continue_to_running_research_team,
        ["planner", "researcher", "coder"],
    )

    # 添加从报告者到结束的边，表示流程结束
    builder.add_edge("reporter", END)

    return builder


def build_graph_with_memory():
    """
    构建并返回带有内存功能的智能体工作流图

    创建一个具有持久化记忆功能的工作流图，能够保存对话历史。
    这对于需要记住上下文的多轮对话非常重要。

    返回:
        编译好的、带有内存功能的工作流图
    """
    # 使用持久化内存保存对话历史
    # TODO: 兼容 SQLite / PostgreSQL 数据库存储
    memory = MemorySaver()

    # 构建状态图
    builder = _build_base_graph()
    # 编译并添加检查点保存器
    return builder.compile(checkpointer=memory)


def build_graph():
    """
    构建并返回不带内存功能的智能体工作流图

    创建一个基本的工作流图，没有持久化记忆功能。
    适用于不需要长期记忆上下文的简单场景。

    返回:
        编译好的工作流图
    """
    # 构建状态图
    builder = _build_base_graph()
    # 编译并返回
    return builder.compile()


# 创建默认的工作流图实例
graph = build_graph()
