from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import hashlib

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User, APIKey

bearer_scheme = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def get_current_user_or_api_key(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    api_key: str = Security(api_key_header),
    db: AsyncSession = Depends(get_db),
) -> User:
    # Try API key first
    if api_key:
        hashed = hashlib.sha256(api_key.encode()).hexdigest()
        result = await db.execute(select(APIKey).where(APIKey.hashed_key == hashed, APIKey.is_active == True))
        key_record = result.scalar_one_or_none()
        if key_record:
            result2 = await db.execute(select(User).where(User.id == key_record.owner_id))
            user = result2.scalar_one_or_none()
            if user and user.is_active:
                return user
    # Fall back to bearer token
    if credentials:
        return await get_current_user(credentials, db)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    from app.models.user import UserRole
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user
