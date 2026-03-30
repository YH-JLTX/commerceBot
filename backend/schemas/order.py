"""
====================================
代码任务: 订单相关Pydantic模型
最后修改: 2026-03-30 20:00
====================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal
from backend.models.order import OrderStatus


class OrderBase(BaseModel):
    """订单基础模型"""
    order_no: str = Field(..., min_length=1, max_length=100, description="订单编号")


class OrderCreate(BaseModel):
    """创建订单请求"""
    product_id: int = Field(..., description="商品ID")
    platform_order_id: str = Field(..., max_length=100, description="平台订单ID")
    order_no: str = Field(..., max_length=100, description="订单编号")
    total_amount: Decimal = Field(..., gt=0, description="订单总额")
    quantity: int = Field(default=1, ge=1, description="商品数量")
    buyer_name: Optional[str] = Field(None, max_length=50, description="买家姓名")
    buyer_phone: Optional[str] = Field(None, max_length=20, description="买家电话")
    buyer_address: Optional[str] = Field(None, description="买家地址")
    remark: Optional[str] = Field(None, description="订单备注")


class OrderUpdate(BaseModel):
    """更新订单请求"""
    status: Optional[OrderStatus] = Field(None, description="订单状态")
    payment_amount: Optional[Decimal] = Field(None, ge=0, description="实付金额")


class OrderResponse(OrderBase):
    """订单响应"""
    order_id: int
    shop_id: int
    product_id: Optional[int] = None
    platform_order_id: str
    status: OrderStatus
    total_amount: Decimal
    payment_amount: Optional[Decimal] = None
    quantity: int
    buyer_name: Optional[str] = None
    buyer_phone: Optional[str] = None
    buyer_address: Optional[str] = None
    remark: Optional[str] = None
    paid_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
