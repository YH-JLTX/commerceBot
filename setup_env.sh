#!/bin/bash
# ====================================
# 代码任务: Linux/Mac一键安装虚拟环境和依赖
# 最后修改: 2026-03-30 19:00
# ====================================

echo ""
echo "===================================="
echo "智营电商智能体 - 环境初始化脚本"
echo "===================================="
echo ""

# 检查Python版本
echo "[1/5] 检查Python版本..."
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.10+"
    exit 1
fi
python3 --version

# 创建虚拟环境
echo "[2/5] 创建虚拟环境..."
if [ -d "venv" ]; then
    echo "虚拟环境已存在，跳过创建"
else
    python3 -m venv venv
    echo "虚拟环境创建成功"
fi

# 激活虚拟环境
echo "[3/5] 激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "[4/5] 升级pip到最新版本..."
pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装依赖
echo "[5/5] 安装项目依赖包..."
echo "使用清华镜像源加速下载..."
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo ""
echo "===================================="
echo "安装完成！"
echo "===================================="
echo ""
echo "激活虚拟环境命令:"
echo "  source venv/bin/activate"
echo ""
echo "退出虚拟环境命令:"
echo "  deactivate"
echo ""
echo "后续开发请确保虚拟环境已激活"
echo ""
