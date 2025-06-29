# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import os
import dataclasses
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from langgraph.prebuilt.chat_agent_executor import AgentState
from src.config.configuration import Configuration

# 初始化 Jinja2 环境，用于加载和渲染模板文件
# loader 指定模板文件所在目录
# autoescape 自动转义（适用于 HTML/XML，这里可增强安全性）
# trim_blocks/lstrip_blocks 控制模板渲染时的空白处理
env = Environment(
    loader=FileSystemLoader(os.path.dirname(__file__)),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)


def get_prompt_template(prompt_name: str) -> str:
    """
    加载并返回指定名称的 prompt 模板内容（已渲染）。

    参数：
        prompt_name: 模板文件名（不带 .md 后缀）
    返回：
        渲染后的模板字符串
    """
    try:
        # 加载模板文件（假设为 .md 格式）
        template = env.get_template(f"{prompt_name}.md")
        # 渲染模板（此处未传变量，适合无变量模板）
        return template.render()
    except Exception as e:
        # 加载或渲染失败时抛出异常
        raise ValueError(f"Error loading template {prompt_name}: {e}")


def apply_prompt_template(
    prompt_name: str, state: AgentState, configurable: Configuration = None
) -> list:
    """
    将变量应用到指定的 prompt 模板，并返回格式化后的消息列表。

    参数：
        prompt_name: 要使用的模板名称
        state: 当前 agent 的状态，包含用于模板替换的变量
        configurable: 可选的配置对象，补充更多变量
    返回：
        消息列表，第一个为 system prompt，后接历史消息
    """
    # 构建用于模板渲染的变量字典
    state_vars = {
        # 当前时间，格式化为字符串，供模板引用
        "CURRENT_TIME": datetime.now().strftime("%a %b %d %Y %H:%M:%S %z"),
        # 解包 state 字典，包含 agent 的上下文变量
        **state,
    }

    # 如果有额外配置，将其字段合并进变量字典
    if configurable:
        state_vars.update(dataclasses.asdict(configurable))

    try:
        # 加载指定的模板文件
        template = env.get_template(f"{prompt_name}.md")
        # 用变量渲染模板，生成最终的 system prompt
        system_prompt = template.render(**state_vars)
        # 返回消息列表，system prompt 作为第一条，后接历史消息
        return [{"role": "system", "content": system_prompt}] + state["messages"]
    except Exception as e:
        # 渲染或加载失败时抛出异常
        raise ValueError(f"Error applying template {prompt_name}: {e}")
