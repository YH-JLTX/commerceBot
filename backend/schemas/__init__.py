"""
====================================
代码任务: Pydantic模型模块入口
最后修改: 2026-03-30 20:00
====================================
"""

from backend.schemas.user import (
    UserBase, UserCreate, UserLogin, UserResponse,
    Token, TokenPayload
)
from backend.schemas.shop import (
    ShopBase, ShopCreate, ShopUpdate, ShopResponse
)
from backend.schemas.product import (
    ProductBase, ProductCreate, ProductUpdate, ProductResponse
)
from backend.schemas.order import (
    OrderBase, OrderCreate, OrderUpdate, OrderResponse, OrderStatus
)
from backend.schemas.logistics import (
    LogisticsBase, LogisticsResponse
)
from backend.schemas.dashboard import (
    DashboardMetrics, TopProduct, RecentOrder
)
from backend.schemas.chat import (
    ChatRequest, ChatResponse, Message
)
from backend.schemas.common import (
    CommonResponse, PageResponse, PageParams
)

__all__ = [
    # User
    "UserBase", "UserCreate", "UserLogin", "UserResponse",
    "Token", "TokenPayload",
    # Shop
    "ShopBase", "ShopCreate", "ShopUpdate", "ShopResponse",
    # Product
    "ProductBase", "ProductCreate", "ProductUpdate", "ProductResponse",
    # Order
    "OrderBase", "OrderCreate", "OrderUpdate", "OrderResponse", "OrderStatus",
    # Logistics
    "LogisticsBase", "LogisticsResponse",
    # Dashboard
    "DashboardMetrics", "TopProduct", "RecentOrder",
    # Chat
    "ChatRequest", "ChatResponse", "Message",
    # Common
    "CommonResponse", "PageResponse", "PageParams",
]
