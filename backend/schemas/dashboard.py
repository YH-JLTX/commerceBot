"""
====================================
代码任务: 仪表盘相关Pydantic模型
最后修改: 2026-03-30 20:00
====================================
"""

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from decimal import Decimal


class TopProduct(BaseModel):
    """热销商品"""
    product_id: int
    name: str
    sku: str
    current_price: Decimal
    sales_count: int


class RecentOrder(BaseModel):
    """最近订单"""
    order_id: int
    order_no: str
    total_amount: Decimal
    status: str
    created_at: datetime


class DashboardMetrics(BaseModel):
    """仪表盘指标"""
    gmv: float
    order_count: int
    aov: float
    gmv_growth: float
    order_growth: float
    top_products: List[TopProduct]
    recent_orders: List[RecentOrder]
    low_stock_count: int
    logistics_anomaly_count: int
