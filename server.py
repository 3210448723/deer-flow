# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""
Server script for running the DeerFlow API.
"""

import argparse  # 用于解析命令行参数
import logging   # 用于日志记录
import signal    # 用于处理系统信号，实现优雅关闭
import sys       # 用于系统相关操作，如退出程序
import uvicorn   # 用于运行 ASGI 服务器
import os
import datetime  # 用于获取当前时间戳

# 配置日志记录格式和级别
logging.basicConfig(
    level=logging.INFO,  # 默认日志级别为 INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # 日志输出格式
)

logger = logging.getLogger(__name__)  # 获取当前模块的日志记录器


# 日志文件目录和文件名
log_dir = "logs"
# 日志名称以时间戳命名，避免覆盖
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(log_dir, f"deerflow_api_{timestamp}.log")
os.makedirs(log_dir, exist_ok=True)

# 日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 文件处理器
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def handle_shutdown(signum, frame):
    """处理 SIGTERM/SIGINT 信号，实现优雅关闭"""
    logger.info("收到关闭信号，开始优雅关闭...")
    sys.exit(0)  # 退出程序


# 注册信号处理函数，捕获 SIGTERM 和 SIGINT 信号
signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="运行 DeerFlow API 服务器")
    parser.add_argument(
        "--reload",
        action="store_true",
        help="启用自动重载（默认：True，Windows 下为 False）",
    )
    parser.add_argument(
        "--host",
        type=str,
        # default="localhost",
        default="0.0.0.0",
        help="服务器绑定的主机地址（默认：localhost）",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="服务器绑定的端口号（默认：8000）",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        help="日志级别（默认：info）",
    )

    args = parser.parse_args()  # 解析参数

    # 根据参数决定是否启用自动重载
    reload = False
    if args.reload:
        reload = True

    try:
        # 启动 uvicorn 服务器，加载 src.server:app 应用
        logger.info(f"启动 DeerFlow API 服务器，地址：{args.host}:{args.port}")
        uvicorn.run(
            "src.server:app",  # 指定 ASGI 应用的路径
            host=args.host,     # 绑定主机
            port=args.port,     # 绑定端口
            reload=reload,      # 是否启用自动重载
            log_level=args.log_level,  # 日志级别
        )
        logger.setLevel(args.log_level.upper())  # 设置日志级别
    except Exception as e:
        # 启动失败时输出错误日志并退出
        logger.error(f"服务器启动失败: {str(e)}")
        sys.exit(1)
