"""
====================================
代码任务: ORM模型模块入口
最后修改: 2026-03-30 20:30
====================================
"""

from backend.models.user import User
from backend.models.shop import Shop, ShopType, ShopStatus
from backend.models.product import Product
from backend.models.order import Order, OrderStatus
from backend.models.logistics import Logistics
from backend.models.review import ProductReview
from backend.models.customer import Customer, CustomerLevel
from backend.models.promotion import Promotion, PromotionType, PromotionStatus
from backend.models.analytics import ShopAnalytics

__all__ = [
    "User",
    "Shop",
    "ShopType",
    "ShopStatus",
    "Product",
    "Order",
    "OrderStatus",
    "Logistics",
    "ProductReview",
    "Customer",
    "CustomerLevel",
    "Promotion",
    "PromotionType",
    "PromotionStatus",
    "ShopAnalytics",
]
