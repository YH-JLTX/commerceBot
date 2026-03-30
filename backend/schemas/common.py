"""
====================================
代码任务: 通用Pydantic模型
最后修改: 2026-03-30 20:00
====================================
"""

from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, List

T = TypeVar("T")


class CommonResponse(BaseModel):
    """通用响应"""
    code: int = Field(default=0, description="状态码，0表示成功")
    message: str = Field(default="success", description="响应消息")
    data: Optional[dict] = Field(default=None, description="响应数据")


class PageParams(BaseModel):
    """分页参数"""
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页数量")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PageResponse(BaseModel, Generic[T]):
    """分页响应"""
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")
    items: List[T] = Field(..., description="数据列表")
