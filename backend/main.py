"""
====================================
代码任务: FastAPI应用主入口
最后修改: 2026-03-30 20:00
====================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from contextlib import asynccontextmanager

from backend.core import settings
from backend.database import init_db, close_db
from backend.api.v1 import auth, shops, products, orders, dashboard, chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    print("Starting application...")
    print("Initializing database...")
    await init_db()
    print("Database initialized")
    yield
    # 关闭时清理资源
    print("Shutting down...")
    await close_db()
    print("Resources cleaned up")


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="电商智能运营Agent系统",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(shops.router)
api_router.include_router(products.router)
api_router.include_router(orders.router)
api_router.include_router(dashboard.router)
api_router.include_router(chat.router)

app.include_router(api_router)


@app.get("/")
async def root():
    """根路径"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
