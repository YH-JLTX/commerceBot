"""
====================================
代码任务: 物流ORM模型
最后修改: 2026-03-30 20:00
====================================
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, func
from sqlalchemy.orm import relationship
from backend.database import Base


class Logistics(Base):
    """物流模型"""
    __tablename__ = "logistics"

    logistics_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False, comment="订单ID")
    tracking_number = Column(String(100), nullable=False, comment="物流单号")
    carrier = Column(String(50), nullable=False, comment="物流公司")
    carrier_code = Column(String(20), comment="物流公司代码")
    current_status = Column(String(50), comment="当前状态")
    current_location = Column(String(255), comment="当前位置")
    estimated_delivery = Column(DateTime, comment="预计送达时间")
    actual_delivery = Column(DateTime, comment="实际送达时间")
    tracking_details = Column(JSON, comment="物流轨迹")
    anomaly_detected = Column(Boolean, default=False, comment="是否异常")
    anomaly_type = Column(String(50), comment="异常类型")
    last_sync_at = Column(DateTime, comment="最后同步时间")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    order = relationship("Order", back_populates="logistics")
