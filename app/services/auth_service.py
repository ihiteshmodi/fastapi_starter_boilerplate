from datetime import UTC, datetime, timedelta
import hashlib
import hmac
from typing import Any

import jwt
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import Settings
from app.models import AuthUser


class AuthenticationError(Exception):
    pass


def hash_password(password: str, salt: str) -> str:
    seed = f"{salt}:{password}".encode("utf-8")
    return hashlib.sha256(seed).hexdigest()


def verify_password(*, password: str, password_hash: str, salt: str) -> bool:
    computed = hash_password(password=password, salt=salt)
    return hmac.compare_digest(computed, password_hash)


def issue_access_token(*, subject: str, scope: str, settings: Settings) -> str:
    now = datetime.now(UTC)
    expire_at = now + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    payload: dict[str, Any] = {
        "sub": subject,
        "scope": scope,
        "iat": int(now.timestamp()),
        "exp": int(expire_at.timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str, settings: Settings) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


def authenticate(*, username: str, password: str, session: Session, settings: Settings) -> str:
    user = session.execute(select(AuthUser).where(AuthUser.username == username)).scalar_one_or_none()
    if user is None:
        raise AuthenticationError("Invalid credentials")

    if not verify_password(password=password, password_hash=user.password_hash, salt=settings.auth_password_salt):
        raise AuthenticationError("Invalid credentials")

    return issue_access_token(subject=user.username, scope=user.scope, settings=settings)


__all__ = ["AuthenticationError", "InvalidTokenError", "authenticate", "decode_access_token", "hash_password"]
