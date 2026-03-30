"""
====================================
代码任务: 商品管理API路由
最后修改: 2026-03-30 20:00
====================================
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List, Optional

from backend.database import get_async_session
from backend.models.user import User
from backend.models.product import Product
from backend.models.shop import Shop
from backend.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from backend.api.v1.auth import get_current_user

router = APIRouter(prefix="/products", tags=["商品管理"])


async def verify_shop_access(shop_id: int, user_id: int, session: AsyncSession) -> Shop:
    """验证店铺访问权限"""
    stmt = select(Shop).where(Shop.shop_id == shop_id, Shop.user_id == user_id)
    result = await session.execute(stmt)
    shop = result.scalar_one_or_none()
    if shop is None:
        raise HTTPException(status_code=404, detail="店铺不存在或无权访问")
    return shop


@router.get("/", response_model=List[ProductResponse])
async def list_products(
    shop_id: Optional[int] = Query(None, description="店铺ID"),
    category: Optional[str] = Query(None, description="商品分类"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """获取商品列表"""
    # 获取用户的所有店铺
    shop_stmt = select(Shop.shop_id).where(Shop.user_id == current_user.user_id)
    shop_result = await session.execute(shop_stmt)
    user_shop_ids = [s[0] for s in shop_result.fetchall()]

    # 构建查询
    stmt = select(Product).where(Product.shop_id.in_(user_shop_ids))

    if shop_id:
        if shop_id not in user_shop_ids:
            raise HTTPException(status_code=403, detail="无权访问该店铺")
        stmt = stmt.where(Product.shop_id == shop_id)

    if category:
        stmt = stmt.where(Product.category == category)

    if search:
        stmt = stmt.where(
            or_(
                Product.name.contains(search),
                Product.sku.contains(search),
                Product.brand.contains(search)
            )
        )

    stmt = stmt.order_by(Product.created_at.desc())
    result = await session.execute(stmt)
    products = result.scalars().all()
    return products


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    shop_id: int = Query(..., description="店铺ID"),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """创建新商品"""
    # 验证店铺权限
    await verify_shop_access(shop_id, current_user.user_id, session)

    # 检查SKU是否存在
    stmt = select(Product).where(Product.sku == product_data.sku)
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="SKU已存在")

    product = Product(
        shop_id=shop_id,
        **product_data.model_dump()
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """获取商品详情"""
    # 获取用户的所有店铺
    shop_stmt = select(Shop.shop_id).where(Shop.user_id == current_user.user_id)
    shop_result = await session.execute(shop_stmt)
    user_shop_ids = [s[0] for s in shop_result.fetchall()]

    stmt = select(Product).where(
        Product.product_id == product_id,
        Product.shop_id.in_(user_shop_ids)
    )
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="商品不存在")

    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """更新商品信息"""
    # 获取用户的所有店铺
    shop_stmt = select(Shop.shop_id).where(Shop.user_id == current_user.user_id)
    shop_result = await session.execute(shop_stmt)
    user_shop_ids = [s[0] for s in shop_result.fetchall()]

    stmt = select(Product).where(
        Product.product_id == product_id,
        Product.shop_id.in_(user_shop_ids)
    )
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="商品不存在")

    # 更新字段
    for field, value in product_data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    await session.commit()
    await session.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """删除商品"""
    # 获取用户的所有店铺
    shop_stmt = select(Shop.shop_id).where(Shop.user_id == current_user.user_id)
    shop_result = await session.execute(shop_stmt)
    user_shop_ids = [s[0] for s in shop_result.fetchall()]

    stmt = select(Product).where(
        Product.product_id == product_id,
        Product.shop_id.in_(user_shop_ids)
    )
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=404, detail="商品不存在")

    await session.delete(product)
    await session.commit()
