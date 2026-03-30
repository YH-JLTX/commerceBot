"""
====================================
代码任务: 店铺ORM模型
最后修改: 2026-03-30 20:00
====================================
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, JSON, ForeignKey, func
from sqlalchemy.orm import relationship
from backend.database import Base
import enum


class ShopType(str, enum.Enum):
    """店铺类型枚举"""
    TAOBAO = "taobao"
    JD = "jd"
    PINDUODUO = "pinduoduo"
    OTHER = "other"


class ShopStatus(str, enum.Enum):
    """店铺状态枚举"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class Shop(Base):
    """店铺模型"""
    __tablename__ = "shops"

    shop_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, comment="用户ID")
    shop_name = Column(String(100), nullable=False, comment="店铺名称")
    shop_type = Column(Enum(ShopType), default=ShopType.TAOBAO, comment="店铺类型")
    shop_url = Column(String(255), comment="店铺URL")
    description = Column(Text, comment="店铺描述")
    logo_url = Column(String(255), comment="店铺Logo")
    platform_shop_id = Column(String(100), comment="平台店铺ID")
    status = Column(Enum(ShopStatus), default=ShopStatus.ACTIVE, comment="店铺状态")
    settings = Column(JSON, comment="店铺设置")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    user = relationship("User", back_populates="shops")
    products = relationship("Product", back_populates="shop", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="shop", cascade="all, delete-orphan")
