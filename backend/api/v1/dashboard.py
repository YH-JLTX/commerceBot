"""
====================================
代码任务: 仪表盘API路由
最后修改: 2026-03-30 20:00
====================================
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from typing import List

from backend.database import get_async_session
from backend.models.user import User
from backend.models.shop import Shop
from backend.models.order import Order
from backend.models.product import Product
from backend.models.logistics import Logistics
from backend.schemas.dashboard import DashboardMetrics, TopProduct, RecentOrder
from backend.api.v1.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["仪表盘"])


@router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    shop_id: int = Query(..., description="店铺ID"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """获取仪表盘指标"""
    # 验证店铺权限
    shop_stmt = select(Shop).where(
        Shop.shop_id == shop_id,
        Shop.user_id == current_user.user_id
    )
    shop_result = await session.execute(shop_stmt)
    if shop_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="店铺不存在或无权访问")

    # 计算GMV（最近30天）
    thirty_days_ago = datetime.now() - timedelta(days=30)
    gmv_stmt = select(func.coalesce(func.sum(Order.total_amount), 0)).where(
        Order.shop_id == shop_id,
        Order.created_at >= thirty_days_ago
    )
    gmv_result = await session.execute(gmv_stmt)
    gmv = float(gmv_result.scalar() or 0)

    # 计算GMV增长率（对比上期）
    prev_period_start = thirty_days_ago - timedelta(days=30)
    prev_gmv_stmt = select(func.coalesce(func.sum(Order.total_amount), 0)).where(
        Order.shop_id == shop_id,
        Order.created_at >= prev_period_start,
        Order.created_at < thirty_days_ago
    )
    prev_gmv_result = await session.execute(prev_gmv_stmt)
    prev_gmv = float(prev_gmv_result.scalar() or 0)
    gmv_growth = round((gmv - prev_gmv) / prev_gmv * 100, 2) if prev_gmv > 0 else 0

    # 订单数量
    order_count_stmt = select(func.count(Order.order_id)).where(
        Order.shop_id == shop_id,
        Order.created_at >= thirty_days_ago
    )
    order_count_result = await session.execute(order_count_stmt)
    order_count = order_count_result.scalar() or 0

    # 订单增长率
    prev_order_count_stmt = select(func.count(Order.order_id)).where(
        Order.shop_id == shop_id,
        Order.created_at >= prev_period_start,
        Order.created_at < thirty_days_ago
    )
    prev_order_count_result = await session.execute(prev_order_count_stmt)
    prev_order_count = prev_order_count_result.scalar() or 0
    order_growth = round((order_count - prev_order_count) / prev_order_count * 100, 2) if prev_order_count > 0 else 0

    # 客单价
    aov = round(gmv / order_count, 2) if order_count > 0 else 0

    # 热销商品（按销量排序）
    top_products_stmt = select(Product).where(
        Product.shop_id == shop_id
    ).order_by(Product.sales_count.desc()).limit(5)
    top_products_result = await session.execute(top_products_stmt)
    top_products = [
        TopProduct(
            product_id=p.product_id,
            name=p.name,
            sku=p.sku,
            current_price=float(p.current_price or p.cost_price),
            sales_count=p.sales_count
        )
        for p in top_products_result.scalars().all()
    ]

    # 最近订单
    recent_orders_stmt = select(Order).where(
        Order.shop_id == shop_id
    ).order_by(Order.created_at.desc()).limit(10)
    recent_orders_result = await session.execute(recent_orders_stmt)
    recent_orders = [
        RecentOrder(
            order_id=o.order_id,
            order_no=o.order_no,
            total_amount=float(o.total_amount),
            status=o.status.value,
            created_at=o.created_at
        )
        for o in recent_orders_result.scalars().all()
    ]

    # 库存不足商品数（库存<10）
    low_stock_stmt = select(func.count(Product.product_id)).where(
        Product.shop_id == shop_id,
        Product.stock_count < 10
    )
    low_stock_result = await session.execute(low_stock_stmt)
    low_stock_count = low_stock_result.scalar() or 0

    # 物流异常数
    logistics_anomaly_stmt = select(func.count(Logistics.logistics_id)).join(Order).where(
        Order.shop_id == shop_id,
        Logistics.anomaly_detected == True
    )
    logistics_anomaly_result = await session.execute(logistics_anomaly_stmt)
    logistics_anomaly_count = logistics_anomaly_result.scalar() or 0

    return DashboardMetrics(
        gmv=gmv,
        order_count=order_count,
        aov=aov,
        gmv_growth=gmv_growth,
        order_growth=order_growth,
        top_products=top_products,
        recent_orders=recent_orders,
        low_stock_count=low_stock_count,
        logistics_anomaly_count=logistics_anomaly_count
    )
