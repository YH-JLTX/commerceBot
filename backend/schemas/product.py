"""
====================================
代码任务: 商品相关Pydantic模型
最后修改: 2026-03-30 20:00
====================================
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


class ProductBase(BaseModel):
    """商品基础模型"""
    sku: str = Field(..., min_length=1, max_length=50, description="商品SKU")
    name: str = Field(..., min_length=1, max_length=200, description="商品名称")
    description: Optional[str] = Field(None, description="商品描述")
    category: Optional[str] = Field(None, max_length=50, description="商品分类")
    brand: Optional[str] = Field(None, max_length=50, description="商品品牌")


class ProductCreate(ProductBase):
    """创建商品请求"""
    cost_price: Decimal = Field(..., gt=0, description="成本价")
    current_price: Optional[Decimal] = Field(None, gt=0, description="当前售价")
    original_price: Optional[Decimal] = Field(None, gt=0, description="原价")
    stock_count: int = Field(default=0, ge=0, description="库存数量")
    main_image: Optional[str] = Field(None, max_length=255, description="主图URL")
    images: Optional[List[str]] = Field(default_factory=list, description="图片列表")
    attributes: Optional[dict] = Field(default_factory=dict, description="商品属性")

    @field_validator('sku')
    @classmethod
    def validate_sku(cls, v: str) -> str:
        """验证SKU格式"""
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('SKU只能包含字母、数字、连字符和下划线')
        return v.upper()


class ProductUpdate(BaseModel):
    """更新商品请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="商品名称")
    description: Optional[str] = Field(None, description="商品描述")
    category: Optional[str] = Field(None, max_length=50, description="商品分类")
    brand: Optional[str] = Field(None, max_length=50, description="商品品牌")
    cost_price: Optional[Decimal] = Field(None, gt=0, description="成本价")
    current_price: Optional[Decimal] = Field(None, gt=0, description="当前售价")
    original_price: Optional[Decimal] = Field(None, gt=0, description="原价")
    stock_count: Optional[int] = Field(None, ge=0, description="库存数量")
    main_image: Optional[str] = Field(None, max_length=255, description="主图URL")
    images: Optional[List[str]] = Field(None, description="图片列表")
    attributes: Optional[dict] = Field(None, description="商品属性")
    is_active: Optional[bool] = Field(None, description="是否上架")


class ProductResponse(ProductBase):
    """商品响应"""
    product_id: int
    shop_id: int
    cost_price: Decimal
    current_price: Optional[Decimal] = None
    original_price: Optional[Decimal] = None
    stock_count: int
    sales_count: int
    main_image: Optional[str] = None
    images: Optional[List[str]] = None
    attributes: Optional[dict] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
