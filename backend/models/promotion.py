"""
====================================
代码任务: 促销活动ORM模型
最后修改: 2026-03-30 20:30
====================================
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, DECIMAL, JSON, Boolean, func, Enum
from sqlalchemy.orm import relationship
from backend.database import Base
import enum


class PromotionType(str, enum.Enum):
    """促销类型枚举"""
    DISCOUNT = "discount"          # 折扣
    COUPON = "coupon"              # 优惠券
    FLASH_SALE = "flash_sale"      # 秒杀
    BUNDLE = "bundle"              # 满减
    GIFT = "gift"                  # 赠品
    SHIPPING = "shipping"          # 包邮


class PromotionStatus(str, enum.Enum):
    """促销状态枚举"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    ENDED = "ended"
    CANCELLED = "cancelled"


class Promotion(Base):
    """促销活动模型"""
    __tablename__ = "promotions"

    promotion_id = Column(Integer, primary_key=True, autoincrement=True)
    shop_id = Column(Integer, ForeignKey("shops.shop_id"), nullable=False, comment="店铺ID")

    # 基本信息
    name = Column(String(100), nullable=False, comment="活动名称")
    description = Column(Text, comment="活动描述")
    type = Column(Enum(PromotionType), nullable=False, comment="促销类型")
    status = Column(Enum(PromotionStatus), default=PromotionStatus.DRAFT, comment="活动状态")

    # 活动时间
    start_time = Column(DateTime, comment="开始时间")
    end_time = Column(DateTime, comment="结束时间")

    # 优惠配置
    discount_value = Column(DECIMAL(10, 2), comment="折扣值")
    min_amount = Column(DECIMAL(10, 2), comment="最低消费金额")
    max_discount = Column(DECIMAL(10, 2), comment="最大优惠金额")

    # 适用范围
    applicable_products = Column(JSON, comment="适用商品ID列表")
    applicable_categories = Column(JSON, comment="适用分类列表")

    # 其他配置
    stock_limit = Column(Integer, comment="库存限制")
    per_customer_limit = Column(Integer, comment="每人限购")
    used_count = Column(Integer, default=0, comment="已使用次数")

    # 优先级
    priority = Column(Integer, default=0, comment="优先级")

    # 备注
    remark = Column(String(500), comment="备注")

    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    shop = relationship("Shop", backref="promotions")
