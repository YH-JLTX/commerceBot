"""
====================================
代码任务: 店铺相关Pydantic模型
最后修改: 2026-03-30 20:00
====================================
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from backend.models.shop import ShopType, ShopStatus


class ShopBase(BaseModel):
    """店铺基础模型"""
    shop_name: str = Field(..., min_length=1, max_length=100, description="店铺名称")
    shop_type: ShopType = Field(default=ShopType.TAOBAO, description="店铺类型")
    description: Optional[str] = Field(None, description="店铺描述")


class ShopCreate(ShopBase):
    """创建店铺请求"""
    shop_url: Optional[str] = Field(None, max_length=255, description="店铺URL")
    platform_shop_id: Optional[str] = Field(None, max_length=100, description="平台店铺ID")


class ShopUpdate(BaseModel):
    """更新店铺请求"""
    shop_name: Optional[str] = Field(None, min_length=1, max_length=100, description="店铺名称")
    description: Optional[str] = Field(None, description="店铺描述")
    logo_url: Optional[str] = Field(None, max_length=255, description="店铺Logo")
    status: Optional[ShopStatus] = Field(None, description="店铺状态")


class ShopResponse(ShopBase):
    """店铺响应"""
    shop_id: int
    user_id: int
    shop_url: Optional[str] = None
    logo_url: Optional[str] = None
    platform_shop_id: Optional[str] = None
    status: ShopStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
