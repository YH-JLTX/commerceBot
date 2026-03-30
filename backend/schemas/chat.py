"""
====================================
代码任务: 聊天相关Pydantic模型
最后修改: 2026-03-30 20:00
====================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Literal


class Message(BaseModel):
    """聊天消息"""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """聊天请求"""
    message: str = Field(..., min_length=1, description="用户消息")
    shop_id: Optional[int] = Field(None, description="店铺ID")
    conversation_id: Optional[str] = Field(None, description="会话ID")


class ChatResponse(BaseModel):
    """聊天响应"""
    response: str
    conversation_id: str
    intermediate_steps: Optional[List[dict]] = None
