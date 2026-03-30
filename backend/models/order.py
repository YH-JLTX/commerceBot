"""
====================================
代码任务: 订单ORM模型
最后修改: 2026-03-30 20:00
====================================
"""

from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, ForeignKey, Enum, func
from sqlalchemy.orm import relationship
from backend.database import Base
import enum


class OrderStatus(str, enum.Enum):
    """订单状态枚举"""
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDING = "refunding"


class Order(Base):
    """订单模型"""
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    shop_id = Column(Integer, ForeignKey("shops.shop_id"), nullable=False, comment="店铺ID")
    product_id = Column(Integer, ForeignKey("products.product_id"), comment="商品ID")
    platform_order_id = Column(String(100), nullable=False, comment="平台订单ID")
    order_no = Column(String(100), nullable=False, unique=True, comment="订单编号")
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, comment="订单状态")
    total_amount = Column(DECIMAL(10, 2), nullable=False, comment="订单总额")
    payment_amount = Column(DECIMAL(10, 2), comment="实付金额")
    quantity = Column(Integer, default=1, comment="商品数量")
    buyer_name = Column(String(50), comment="买家姓名")
    buyer_phone = Column(String(20), comment="买家电话")
    buyer_address = Column(Text, comment="买家地址")
    remark = Column(Text, comment="订单备注")
    paid_at = Column(DateTime, comment="付款时间")
    shipped_at = Column(DateTime, comment="发货时间")
    completed_at = Column(DateTime, comment="完成时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    shop = relationship("Shop", back_populates="orders")
    product = relationship("Product")
    logistics = relationship("Logistics", back_populates="order", uselist=False, cascade="all, delete-orphan")
