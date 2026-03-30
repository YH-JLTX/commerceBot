"""
====================================
代码任务: 数据库初始化和测试数据生成
最后修改: 2026-03-30 20:00
====================================
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.database import init_db
from backend.core.seed_data import generate_all_test_data


async def main():
    print("=" * 50)
    print("CommerceBot Backend Initialization")
    print("=" * 50)

    # 初始化数据库表
    print("\nInitializing database tables...")
    await init_db()
    print("Database tables initialized")

    # 生成测试数据
    print("\nGenerating test data...")
    stats = await generate_all_test_data()

    print("\n" + "=" * 50)
    print("Initialization Complete!")
    print("=" * 50)
    print(f"Users: {stats['users']}")
    print(f"Shops: {stats['shops']}")
    print(f"Products: {stats['products']}")
    print(f"Orders: {stats['orders']}")
    print(f"Logistics: {stats['logistics']}")
    print("\nTest Accounts:")
    print("  Username: demo_user   Password: demo123")
    print("  Username: test_user1  Password: password123")
    print("\nStart backend server:")
    print("  python -m uvicorn backend.main:app --host 0.0.0.0 --port 8765 --reload")


if __name__ == "__main__":
    asyncio.run(main())
