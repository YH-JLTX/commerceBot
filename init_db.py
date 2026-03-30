"""
====================================
代码任务: 数据库初始化脚本
最后修改: 2026-03-30 20:00
====================================
"""

import asyncio
import aiomysql
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def create_database():
    """创建数据库"""
    print("正在连接MySQL服务器...")

    # 连接MySQL服务器（不指定数据库）
    conn = await aiomysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        charset='utf8mb4'
    )

    try:
        async with conn.cursor() as cursor:
            # 创建数据库
            await cursor.execute(
                "CREATE DATABASE IF NOT EXISTS commerce_bot "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            print("✅ 数据库 'commerce_bot' 创建成功")

            # 显示数据库
            await cursor.execute("SHOW DATABASES LIKE 'commerce_bot'")
            result = await cursor.fetchone()
            print(f"✅ 数据库信息: {result}")

    finally:
        await conn.close()


async def main():
    print("=" * 50)
    print("CommerceBot 数据库初始化")
    print("=" * 50)
    print()

    try:
        await create_database()
        print("\n数据库初始化完成！")
        print("\n下一步: 运行 'python start_backend.py' 生成测试数据")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("\n请确保:")
        print("1. MySQL服务已启动")
        print("2. 用户名: root, 密码: 123456")
        print("3. 如果密码不同，请修改 backend/database/__init__.py 中的 DATABASE_URL")


if __name__ == "__main__":
    asyncio.run(main())
