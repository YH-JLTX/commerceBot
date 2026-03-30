"""
====================================
代码任务: 用户ORM模型
最后修改: 2026-03-30 20:00
====================================
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, func
from sqlalchemy.orm import relationship
from backend.database import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True, comment="用户名")
    email = Column(String(100), nullable=False, unique=True, comment="邮箱")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    phone = Column(String(20), comment="手机号")
    avatar_url = Column(String(255), comment="头像URL")
    notification_settings = Column(JSON, comment="通知设置")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    shops = relationship("Shop", back_populates="user", cascade="all, delete-orphan")
