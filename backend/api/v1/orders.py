"""
====================================
代码任务: 订单管理API路由
最后修改: 2026-03-30 20:00
====================================
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from typing import List, Optional
from datetime import datetime, timedelta

from backend.database import get_async_session
from backend.models.user import User
from backend.models.order import Order, OrderStatus
from backend.models.shop import Shop
from backend.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from backend.api.v1.auth import get_current_user

router = APIRouter(prefix="/orders", tags=["订单管理"])


async def verify_shop_access(shop_id: int, user_id: int, session: AsyncSession) -> Shop:
    """验证店铺访问权限"""
    stmt = select(Shop).where(Shop.shop_id == shop_id, Shop.user_id == user_id)
    result = await session.execute(stmt)
    shop = result.scalar_one_or_none()
    if shop is None:
        raise HTTPException(status_code=404, detail="店铺不存在或无权访问")
    return shop


@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    shop_id: Optional[int] = Query(None, description="店铺ID"),
    status: Optional[OrderStatus] = Query(None, description="订单状态"),
    search: Optional[str] = Query(None, description="搜索关键词（订单号/买家姓名/手机号）"),
    days: Optional[int] = Query(None, description="最近N天的订单"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """获取订单列表"""
    # 获取用户的所有店铺
    shop_stmt = select(Shop.shop_id).where(Shop.user_id == current_user.user_id)
    shop_result = await session.execute(shop_stmt)
    user_shop_ids = [s[0] for s in shop_result.fetchall()]

    # 构建查询
    stmt = select(Order).where(Order.shop_id.in_(user_shop_ids))

    if shop_id:
        if shop_id not in user_shop_ids:
            raise HTTPException(status_code=403, detail="无权访问该店铺")
        stmt = stmt.where(Order.shop_id == shop_id)

    if status:
        stmt = stmt.where(Order.status == status)

    if search:
        stmt = stmt.where(
            or_(
                Order.order_no.contains(search),
                Order.buyer_name.contains(search),
                Order.buyer_phone.contains(search)
            )
        )

    if days:
        start_date = datetime.now() - timedelta(days=days)
        stmt = stmt.where(Order.created_at >= start_date)

    stmt = stmt.order_by(Order.created_at.desc())
    result = await session.execute(stmt)
    orders = result.scalars().all()
    return orders


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    shop_id: int = Query(..., description="店铺ID"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """创建新订单"""
    # 验证店铺权限
    await verify_shop_access(shop_id, current_user.user_id, session)

    # 检查订单号是否存在
    stmt = select(Order).where(Order.order_no == order_data.order_no)
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="订单号已存在")

    order = Order(
        shop_id=shop_id,
        **order_data.model_dump()
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """获取订单详情"""
    # 获取用户的所有店铺
    shop_stmt = select(Shop.shop_id).where(Shop.user_id == current_user.user_id)
    shop_result = await session.execute(shop_stmt)
    user_shop_ids = [s[0] for s in shop_result.fetchall()]

    stmt = select(Order).where(
        Order.order_id == order_id,
        Order.shop_id.in_(user_shop_ids)
    )
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail="订单不存在")

    return order


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """更新订单信息"""
    # 获取用户的所有店铺
    shop_stmt = select(Shop.shop_id).where(Shop.user_id == current_user.user_id)
    shop_result = await session.execute(shop_stmt)
    user_shop_ids = [s[0] for s in shop_result.fetchall()]

    stmt = select(Order).where(
        Order.order_id == order_id,
        Order.shop_id.in_(user_shop_ids)
    )
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail="订单不存在")

    # 更新字段
    for field, value in order_data.model_dump(exclude_unset=True).items():
        setattr(order, field, value)

        # 自动更新时间戳
        if field == "status" and value == OrderStatus.PAID and not order.paid_at:
            order.paid_at = datetime.now()
        elif field == "status" and value == OrderStatus.SHIPPED and not order.shipped_at:
            order.shipped_at = datetime.now()
        elif field == "status" and value == OrderStatus.COMPLETED and not order.completed_at:
            order.completed_at = datetime.now()

    await session.commit()
    await session.refresh(order)
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """删除订单"""
    # 获取用户的所有店铺
    shop_stmt = select(Shop.shop_id).where(Shop.user_id == current_user.user_id)
    shop_result = await session.execute(shop_stmt)
    user_shop_ids = [s[0] for s in shop_result.fetchall()]

    stmt = select(Order).where(
        Order.order_id == order_id,
        Order.shop_id.in_(user_shop_ids)
    )
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail="订单不存在")

    await session.delete(order)
    await session.commit()
