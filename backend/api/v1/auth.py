"""
====================================
代码任务: 认证相关API路由
最后修改: 2026-03-30 20:00
====================================
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from jose import jwt

from backend.database import get_async_session
from backend.models.user import User
from backend.schemas.user import UserCreate, UserLogin, UserResponse, Token, TokenPayload
from backend.core import settings

router = APIRouter(prefix="/auth", tags=["认证"])
security = HTTPBearer()


def create_access_token(user_id: int) -> str:
    """创建访问令牌"""
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "user_id": user_id,
        "exp": expire
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """获取当前用户"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="无效的认证凭证")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="无效的认证凭证")

    stmt = select(User).where(User.user_id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="用户不存在")

    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """用户注册"""
    # 检查用户名是否存在
    stmt = select(User).where(User.username == user_data.username)
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 检查邮箱是否存在
    stmt = select(User).where(User.email == user_data.email)
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="邮箱已被注册")

    # 创建用户
    import hashlib
    password_hash = hashlib.sha256(user_data.password.encode()).hexdigest()

    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
        phone=user_data.phone
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    session: AsyncSession = Depends(get_async_session)
):
    """用户登录"""
    import hashlib
    password_hash = hashlib.sha256(login_data.password.encode()).hexdigest()

    # 查找用户（支持用户名或邮箱登录）
    stmt = select(User).where(
        (User.username == login_data.username) | (User.email == login_data.username)
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None or user.password_hash != password_hash:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="账户已被禁用")

    # 生成Token
    access_token = create_access_token(user.user_id)

    return Token(
        access_token=access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息"""
    return current_user
