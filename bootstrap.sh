#!/bin/bash

# 启动 DeerFlow 的后端和 Web UI 服务器。
# 如果用户按下 Ctrl+C，则同时杀死这两个进程。

# 检查第一个参数是否为开发模式的标志（--dev、-d、dev、development）
if [ "$1" = "--dev" -o "$1" = "-d" -o "$1" = "dev" -o "$1" = "development" ]; then
  # 输出开发模式启动信息
  echo -e "Starting DeerFlow in [DEVELOPMENT] mode...\n"
  # 后台启动后端服务（支持热重载），并保存其进程号到 SERVER_PID
  uv run server.py --reload & SERVER_PID=$$!
  # 进入 web 目录，后台启动前端开发服务器，并保存其进程号到 WEB_PID
  cd web && pnpm dev & WEB_PID=$$!
  # 捕获 SIGINT（Ctrl+C）和 SIGTERM 信号，杀死后端和前端进程
  trap "kill $$SERVER_PID $$WEB_PID" SIGINT SIGTERM
  # 等待所有后台进程结束
  wait
else
  # 输出生产模式启动信息
  echo -e "Starting DeerFlow in [PRODUCTION] mode...\n"
  # 后台启动后端服务（无热重载），并保存其进程号到 SERVER_PID
  uv run server.py & SERVER_PID=$$!
  # 进入 web 目录，后台启动前端生产服务器，并保存其进程号到 WEB_PID
  cd web && pnpm start & WEB_PID=$$!
  # 捕获 SIGINT（Ctrl+C）和 SIGTERM 信号，杀死后端和前端进程
  trap "kill $$SERVER_PID $$WEB_PID" SIGINT SIGTERM
  # 等待所有后台进程结束
  wait
fi
