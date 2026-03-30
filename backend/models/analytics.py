"""
====================================
代码任务: 店铺统计ORM模型
最后修改: 2026-03-30 20:30
====================================
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, JSON, func
from backend.database import Base


class ShopAnalytics(Base):
    """店铺统计数据模型（按天汇总）"""
    __tablename__ = "shop_analytics"

    analytics_id = Column(Integer, primary_key=True, autoincrement=True)
    shop_id = Column(Integer, ForeignKey("shops.shop_id"), nullable=False, comment="店铺ID")

    # 统计日期
    stat_date = Column(DateTime, nullable=False, comment="统计日期")
    stat_type = Column(String(20), default="daily", comment="统计类型：daily/weekly/monthly")

    # 流量指标
    page_views = Column(Integer, default=0, comment="页面浏览量")
    unique_visitors = Column(Integer, default=0, comment="独立访客数")

    # 销售指标
    gmv = Column(DECIMAL(12, 2), default=0, comment="GMV")
    order_count = Column(Integer, default=0, comment="订单数")
    paid_order_count = Column(Integer, default=0, comment="已付款订单数")
    completed_order_count = Column(Integer, default=0, comment="已完成订单数")
    cancelled_order_count = Column(Integer, default=0, comment="已取消订单数")

    # 商品指标
    product_views = Column(Integer, default=0, comment="商品浏览量")
    add_to_cart_count = Column(Integer, default=0, comment="加购次数")
    favorite_count = Column(Integer, default=0, comment="收藏次数")

    # 客单价指标
    aov = Column(DECIMAL(10, 2), comment="客单价")

    # 转化率
    conversion_rate = Column(DECIMAL(5, 4), comment="转化率")
    pay_conversion_rate = Column(DECIMAL(5, 4), comment="付款转化率")

    # 客户指标
    new_customer_count = Column(Integer, default=0, comment="新客户数")
    returning_customer_count = Column(Integer, default=0, comment="回头客数")

    # 退款指标
    refund_amount = Column(DECIMAL(12, 2), default=0, comment="退款金额")
    refund_order_count = Column(Integer, default=0, comment="退款订单数")

    # 物流指标
    avg_ship_time = Column(Integer, comment="平均发货时长（小时）")
    late_ship_count = Column(Integer, default=0, comment="延迟发货订单数")

    # 额外数据（JSON格式存储灵活指标）
    extra_data = Column(JSON, comment="额外数据")

    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
