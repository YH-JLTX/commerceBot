"""
====================================
代码任务: 店铺管理API路由
最后修改: 2026-03-30 20:00
====================================
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from backend.database import get_async_session
from backend.models.user import User
from backend.models.shop import Shop
from backend.schemas.shop import ShopCreate, ShopUpdate, ShopResponse
from backend.api.v1.auth import get_current_user

router = APIRouter(prefix="/shops", tags=["店铺管理"])


@router.get("/", response_model=List[ShopResponse])
async def list_shops(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """获取当前用户的店铺列表"""
    stmt = select(Shop).where(Shop.user_id == current_user.user_id)
    result = await session.execute(stmt)
    shops = result.scalars().all()
    return shops


@router.post("/", response_model=ShopResponse, status_code=status.HTTP_201_CREATED)
async def create_shop(
    shop_data: ShopCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """创建新店铺"""
    shop = Shop(
        user_id=current_user.user_id,
        **shop_data.model_dump()
    )
    session.add(shop)
    await session.commit()
    await session.refresh(shop)
    return shop


@router.get("/{shop_id}", response_model=ShopResponse)
async def get_shop(
    shop_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """获取店铺详情"""
    stmt = select(Shop).where(
        Shop.shop_id == shop_id,
        Shop.user_id == current_user.user_id
    )
    result = await session.execute(stmt)
    shop = result.scalar_one_or_none()

    if shop is None:
        raise HTTPException(status_code=404, detail="店铺不存在")

    return shop


@router.put("/{shop_id}", response_model=ShopResponse)
async def update_shop(
    shop_id: int,
    shop_data: ShopUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """更新店铺信息"""
    stmt = select(Shop).where(
        Shop.shop_id == shop_id,
        Shop.user_id == current_user.user_id
    )
    result = await session.execute(stmt)
    shop = result.scalar_one_or_none()

    if shop is None:
        raise HTTPException(status_code=404, detail="店铺不存在")

    # 更新字段
    for field, value in shop_data.model_dump(exclude_unset=True).items():
        setattr(shop, field, value)

    await session.commit()
    await session.refresh(shop)
    return shop


@router.delete("/{shop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shop(
    shop_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """删除店铺"""
    stmt = select(Shop).where(
        Shop.shop_id == shop_id,
        Shop.user_id == current_user.user_id
    )
    result = await session.execute(stmt)
    shop = result.scalar_one_or_none()

    if shop is None:
        raise HTTPException(status_code=404, detail="店铺不存在")

    await session.delete(shop)
    await session.commit()
