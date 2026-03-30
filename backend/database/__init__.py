"""
====================================
代码任务: 数据库连接配置模块
最后修改: 2026-03-30 20:00
====================================
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
import os

# 数据库配置
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite+aiosqlite:///commerce_bot.db"
)

# 根据数据库类型选择引擎参数
if DATABASE_URL.startswith("sqlite"):
    # SQLite配置
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False}
    )
else:
    # MySQL配置
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600
    )

# 创建异步会话工厂
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    """ORM基类"""
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """获取异步会话（依赖注入）"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """初始化数据库表"""
    async with engine.begin() as conn:
        # 导入所有模型
        from backend.models.user import User
        from backend.models.shop import Shop
        from backend.models.product import Product
        from backend.models.order import Order
        from backend.models.logistics import Logistics

        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """关闭数据库连接"""
    await engine.dispose()
