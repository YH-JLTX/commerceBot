#!/bin/bash
# ====================================
# 代码任务: Linux/Mac启动脚本
# 最后修改: 2026-03-30 19:00
# ====================================

echo ""
echo "===================================="
echo "智营电商智能体 - 启动服务"
echo "===================================="
echo ""

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "错误: 虚拟环境不存在"
    echo "请先运行: bash setup_env.sh"
    exit 1
fi

# 激活虚拟环境
echo "[1/3] 激活虚拟环境..."
source venv/bin/activate

# 检查.env文件
echo "[2/3] 检查环境配置..."
if [ ! -f ".env" ]; then
    echo "复制环境配置模板..."
    cp .env.example .env
    echo ""
    echo "警告: 请先编辑 .env 文件配置数据库密码等敏感信息"
    echo "配置完成后重新运行此脚本"
    exit 0
fi

# 启动后端服务
echo "[3/3] 启动后端服务..."
echo ""
echo "===================================="
echo "后端服务启动中..."
echo "API地址: http://localhost:8765"
echo "API文档: http://localhost:8765/docs"
echo "按 Ctrl+C 停止服务"
echo "===================================="
echo ""

python -m uvicorn backend.main:app --host 0.0.0.0 --port 8765 --reload
