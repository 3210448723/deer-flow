# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""
DeerFlow 项目的入口脚本。
以命令行的方式回答用户输入。
"""

import argparse
import asyncio

from InquirerPy import inquirer

from src.config.questions import BUILT_IN_QUESTIONS, BUILT_IN_QUESTIONS_ZH_CN
from src.workflow import run_agent_workflow_async


def ask(
    question,
    debug=False,
    max_plan_iterations=1,
    max_step_num=3,
    enable_background_investigation=True,
):
    """
    运行智能体工作流，处理用户输入的问题。
    Run the agent workflow with the given question.

    参数说明：
        question: 用户的查询或请求
        debug: 如果为 True，启用调试级别日志
        max_plan_iterations: 计划最大迭代次数
        max_step_num: 单次计划的最大步骤数
        enable_background_investigation: 如果为 True，规划前先进行网络检索以增强上下文
    """
    asyncio.run(
        run_agent_workflow_async(
            user_input=question,
            debug=debug,
            max_plan_iterations=max_plan_iterations,
            max_step_num=max_step_num,
            enable_background_investigation=enable_background_investigation,
        )
    )


def main(
    debug=False,
    max_plan_iterations=1,
    max_step_num=3,
    enable_background_investigation=True,
):
    """
    交互模式：通过内置问题与用户交互。

    参数说明：
        enable_background_investigation: 是否在规划前进行网络检索以增强上下文
        debug: 是否启用调试日志
        max_plan_iterations: 计划最大迭代次数
        max_step_num: 单次计划的最大步骤数
    """
    # 首先选择语言
    # First select language
    language = inquirer.select(
        message="Select language / 选择语言:",
        choices=["English", "中文"],
    ).execute()

    # 根据语言选择问题列表
    # Choose questions based on language
    questions = (
        BUILT_IN_QUESTIONS if language == "English" else BUILT_IN_QUESTIONS_ZH_CN
    )
    ask_own_option = (
        "[Ask my own question]" if language == "English" else "[自定义问题]"
    )

    # 选择一个问题
    # Select a question
    initial_question = inquirer.select(
        message=(
            "What do you want to know?" if language == "English" else "您想了解什么?"
        ),
        choices=[ask_own_option] + questions,
    ).execute()

    # 如果选择自定义问题，则让用户输入
    if initial_question == ask_own_option:
        initial_question = inquirer.text(
            message=(
                "What do you want to know?"
                if language == "English"
                else "您想了解什么?"
            ),
        ).execute()

    # 将所有参数传递给 ask 函数
    ask(
        question=initial_question,
        debug=debug,
        max_plan_iterations=max_plan_iterations,
        max_step_num=max_step_num,
        enable_background_investigation=enable_background_investigation,
    )


if __name__ == "__main__":
    # 设置命令行参数解析器
    parser = argparse.ArgumentParser(description="Run the Deer")
    parser.add_argument("query", nargs="*", help="要处理的查询内容 (The query to process)")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="以交互模式运行，使用内置问题 (Run in interactive mode with built-in questions)",
    )
    parser.add_argument(
        "--max_plan_iterations",
        type=int,
        default=1,
        help="计划最大迭代次数 (Maximum number of plan iterations, default: 1)",
    )
    parser.add_argument(
        "--max_step_num",
        type=int,
        default=3,
        help="单次计划的最大步骤数 (Maximum number of steps in a plan, default: 3)",
    )
    parser.add_argument("--debug", action="store_true", help="启用调试日志 (Enable debug logging)")
    parser.add_argument(
        "--no-background-investigation",
        action="store_false",
        dest="enable_background_investigation",
        help="禁用规划前的背景调查 (Disable background investigation before planning)",
    )

    args = parser.parse_args()

    # 如果指定了 --interactive，则进入交互模式
    if args.interactive:
        # 将命令行参数传递给 main 函数
        main(
            debug=args.debug,
            max_plan_iterations=args.max_plan_iterations,
            max_step_num=args.max_step_num,
            enable_background_investigation=args.enable_background_investigation,
        )
    else:
        # 从命令行参数或用户输入中解析用户查询
        if args.query:
            user_query = " ".join(args.query)
        else:
            # Loop until user provides non-empty input
            while True:
                user_query = input("Enter your query: ")
                if user_query is not None and user_query != "":
                    break

        # 使用提供的参数运行智能体工作流
        ask(
            question=user_query,
            debug=args.debug,
            max_plan_iterations=args.max_plan_iterations,
            max_step_num=args.max_step_num,
            enable_background_investigation=args.enable_background_investigation,
        )
