"""
====================================
代码任务: 客户ORM模型
最后修改: 2026-03-30 20:30
====================================
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, func, Enum
from sqlalchemy.orm import relationship
from backend.database import Base
import enum


class CustomerLevel(str, enum.Enum):
    """客户等级枚举"""
    NORMAL = "normal"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"


class Customer(Base):
    """客户模型"""
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    shop_id = Column(Integer, ForeignKey("shops.shop_id"), nullable=False, comment="店铺ID")

    # 客户信息
    name = Column(String(50), comment="客户姓名")
    phone = Column(String(20), comment="手机号")
    email = Column(String(100), comment="邮箱")
    wechat = Column(String(50), comment="微信号")
    avatar = Column(String(255), comment="头像URL")

    # 地址信息
    province = Column(String(50), comment="省份")
    city = Column(String(50), comment="城市")
    district = Column(String(50), comment="区县")
    address = Column(String(255), comment="详细地址")

    # 客户等级
    level = Column(Enum(CustomerLevel), default=CustomerLevel.NORMAL, comment="客户等级")

    # 统计数据
    total_orders = Column(Integer, default=0, comment="订单总数")
    total_amount = Column(Integer, default=0, comment="消费总额（分）")
    avg_order_amount = Column(Integer, default=0, comment="平均订单金额（分）")
    last_order_at = Column(DateTime, comment="最后下单时间")

    # 标签和备注
    tags = Column(JSON, comment="客户标签")
    remark = Column(String(500), comment="备注")

    # 首次购买时间
    first_purchase_at = Column(DateTime, comment="首次购买时间")

    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    shop = relationship("Shop", backref="customers")
