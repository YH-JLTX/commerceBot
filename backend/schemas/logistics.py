"""
====================================
代码任务: 物流相关Pydantic模型
最后修改: 2026-03-30 20:00
====================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict


class LogisticsBase(BaseModel):
    """物流基础模型"""
    tracking_number: str = Field(..., description="物流单号")
    carrier: str = Field(..., max_length=50, description="物流公司")


class LogisticsResponse(LogisticsBase):
    """物流响应"""
    logistics_id: int
    order_id: int
    carrier_code: Optional[str] = None
    current_status: Optional[str] = None
    current_location: Optional[str] = None
    estimated_delivery: Optional[datetime] = None
    actual_delivery: Optional[datetime] = None
    tracking_details: Optional[List[Dict]] = None
    anomaly_detected: bool
    anomaly_type: Optional[str] = None
    last_sync_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
