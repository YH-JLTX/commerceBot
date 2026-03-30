"""
====================================
代码任务: 商品ORM模型
最后修改: 2026-03-30 20:00
====================================
"""

from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from backend.database import Base


class Product(Base):
    """商品模型"""
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    shop_id = Column(Integer, ForeignKey("shops.shop_id"), nullable=False, comment="店铺ID")
    sku = Column(String(50), nullable=False, comment="商品SKU")
    name = Column(String(200), nullable=False, comment="商品名称")
    description = Column(Text, comment="商品描述")
    category = Column(String(50), comment="商品分类")
    brand = Column(String(50), comment="商品品牌")
    cost_price = Column(DECIMAL(10, 2), nullable=False, comment="成本价")
    current_price = Column(DECIMAL(10, 2), comment="当前售价")
    original_price = Column(DECIMAL(10, 2), comment="原价")
    stock_count = Column(Integer, default=0, comment="库存数量")
    sales_count = Column(Integer, default=0, comment="销量")
    main_image = Column(String(255), comment="主图URL")
    images = Column(JSON, comment="图片列表")
    attributes = Column(JSON, comment="商品属性")
    is_active = Column(Boolean, default=True, comment="是否上架")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    shop = relationship("Shop", back_populates="products")
