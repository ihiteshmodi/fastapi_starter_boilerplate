from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AuthUser
from app.schemas import Principal
from app.services.auth_service import InvalidTokenError, decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def _credentials_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_db_session(request: Request) -> Session:
    session_factory = request.app.state.db_session_factory
    return session_factory()


def get_current_user(
    request: Request,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> Principal:
    session = get_db_session(request)
    try:
        try:
            payload = decode_access_token(token=token, settings=request.app.state.settings)
        except InvalidTokenError as exc:
            raise _credentials_error() from exc

        username = payload.get("sub")
        if not isinstance(username, str) or not username:
            raise _credentials_error()

        user = session.execute(select(AuthUser).where(AuthUser.username == username)).scalar_one_or_none()
        if user is None:
            raise _credentials_error()

        return Principal(username=user.username, scope=user.scope)
    finally:
        session.close()


def require_basic_or_premium(
    current_user: Annotated[Principal, Depends(get_current_user)],
) -> Principal:
    if current_user.scope not in {"basic", "premium"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    return current_user


def require_premium(
    current_user: Annotated[Principal, Depends(get_current_user)],
) -> Principal:
    if current_user.scope != "premium":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    return current_user
