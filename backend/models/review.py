"""
====================================
代码任务: 商品评价ORM模型
最后修改: 2026-03-30 20:30
====================================
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from backend.database import Base
import enum


class ReviewStatus(str, enum.Enum):
    """评价状态枚举"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ProductReview(Base):
    """商品评价模型"""
    __tablename__ = "product_reviews"

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False, comment="商品ID")
    shop_id = Column(Integer, ForeignKey("shops.shop_id"), nullable=False, comment="店铺ID")
    order_id = Column(Integer, ForeignKey("orders.order_id"), comment="订单ID")

    # 评价内容
    rating = Column(Integer, nullable=False, comment="评分1-5")
    content = Column(Text, comment="评价内容")
    images = Column(JSON, comment="评价图片")

    # 客户信息（匿名）
    buyer_name = Column(String(50), comment="买家昵称")
    buyer_avatar = Column(String(255), comment="买家头像")

    # 商家回复
    seller_reply = Column(Text, comment="商家回复")
    replied_at = Column(DateTime, comment="回复时间")

    # 状态
    status = Column(String(20), default="approved", comment="评价状态")

    # 标签
    tags = Column(JSON, comment="评价标签")

    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    product = relationship("Product", backref="reviews")
