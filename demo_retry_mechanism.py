# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""
JSON格式错误重试机制演示脚本
演示如何在大模型返回格式错误的JSON时自动重试
"""

import json
import logging
from src.config.configuration import Configuration
from src.graph.nodes import _attempt_json_parse_with_retry

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def demo_retry_mechanism():
    """演示重试机制的工作原理"""
    print("=" * 60)
    print("JSON格式错误重试机制演示")
    print("=" * 60)
    
    # 配置
    config = Configuration(max_retry_attempts=3)
    
    # 测试用例1：有效的JSON
    print("\n📋 测试用例1: 有效的JSON")
    valid_json = """
    {
        "locale": "zh-CN",
        "has_enough_context": false,
        "title": "量子计算对加密技术的影响研究",
        "thought": "用户想了解量子计算技术对现有加密方法的潜在威胁。",
        "steps": [
            {
                "need_search": true,
                "title": "量子计算基础原理",
                "description": "研究量子计算的基本原理和工作机制",
                "step_type": "research"
            }
        ]
    }
    """
    
    result, should_retry = _attempt_json_parse_with_retry(valid_json, 0, config)
    print(f"✅ 解析结果: 成功")
    print(f"   是否需要重试: {should_retry}")
    print(f"   解析得到的标题: {result['title'] if result else 'None'}")
    
    # 测试用例2：无效的JSON（缺少右括号）
    print("\n📋 测试用例2: 无效的JSON - 缺少右括号")
    invalid_json1 = """
    {
        "locale": "zh-CN",
        "has_enough_context": false,
        "title": "量子计算对加密技术的影响研究",
        "thought": "用户想了解量子计算技术对现有加密方法的潜在威胁。"
    """  # 故意缺少右括号
    
    result, should_retry = _attempt_json_parse_with_retry(invalid_json1, 0, config)
    print(f"❌ 解析结果: 失败")
    print(f"   是否需要重试: {should_retry}")
    print(f"   原因: JSON格式错误 - 缺少右括号")
    
    # 测试用例3：无效的JSON（多余的逗号）
    print("\n📋 测试用例3: 无效的JSON - 多余的逗号")
    invalid_json2 = """
    {
        "locale": "zh-CN",
        "has_enough_context": false,
        "title": "量子计算对加密技术的影响研究",
        "thought": "用户想了解量子计算技术对现有加密方法的潜在威胁。",
    }
    """  # 故意在最后一个字段后加逗号
    
    result, should_retry = _attempt_json_parse_with_retry(invalid_json2, 0, config)
    print(f"❌ 解析结果: 失败")
    print(f"   是否需要重试: {should_retry}")
    print(f"   原因: JSON格式错误 - 多余的逗号")
    
    # 测试用例4：已有计划迭代时的行为
    print("\n📋 测试用例4: 已有计划迭代时不重试")
    result, should_retry = _attempt_json_parse_with_retry(invalid_json1, 1, config)  # plan_iterations = 1
    print(f"❌ 解析结果: 失败")
    print(f"   是否需要重试: {should_retry}")
    print(f"   原因: 已有计划迭代，不再重试")
    
    # 模拟重试流程
    print("\n🔄 模拟重试流程")
    print("-" * 40)
    
    retry_count = 0
    max_retries = config.max_retry_attempts
    
    test_responses = [
        '{"locale": "zh-CN", "invalid": json}',  # 第1次：无效JSON
        '{"locale": "zh-CN", "title": "Test", missing_quote: "value"}',  # 第2次：无效JSON  
        '{"locale": "zh-CN", "has_enough_context": true, "title": "成功的计划", "thought": "这次成功了"}',  # 第3次：有效JSON
    ]
    
    for i, response in enumerate(test_responses):
        retry_count = i
        print(f"\n尝试第 {retry_count + 1} 次:")
        print(f"LLM响应: {response[:50]}...")
        
        result, should_retry = _attempt_json_parse_with_retry(response, 0, config)
        
        if result:
            print(f"✅ 成功！解析得到计划: {result.get('title', 'Unknown')}")
            print(f"总重试次数: {retry_count}")
            break
        elif should_retry and retry_count < max_retries - 1:
            print(f"❌ 失败，准备重试... (重试次数: {retry_count + 1}/{max_retries})")
        else:
            print(f"❌ 失败，已达最大重试次数或不应重试")
            break
    
    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)

if __name__ == "__main__":
    demo_retry_mechanism()
