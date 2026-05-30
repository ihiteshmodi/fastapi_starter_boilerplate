from collections.abc import Generator

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from app.models import AuthUser, Base
from app.services.auth_service import hash_password


def _is_sqlite(url: str) -> bool:
    return url.startswith("sqlite")


def create_session_factory(database_url: str) -> sessionmaker[Session]:
    connect_args = {"check_same_thread": False} if _is_sqlite(database_url) else {}
    engine = create_engine(database_url, future=True, connect_args=connect_args)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def seed_demo_users(
    session_factory: sessionmaker[Session],
    *,
    basic_username: str,
    basic_password: str,
    premium_username: str,
    premium_password: str,
    salt: str,
) -> None:
    session = session_factory()
    try:
        existing = {
            user.username
            for user in session.execute(select(AuthUser)).scalars().all()
        }

        pending: list[AuthUser] = []
        if basic_username not in existing:
            pending.append(
                AuthUser(
                    username=basic_username,
                    password_hash=hash_password(basic_password, salt),
                    scope="basic",
                )
            )
        if premium_username not in existing:
            pending.append(
                AuthUser(
                    username=premium_username,
                    password_hash=hash_password(premium_password, salt),
                    scope="premium",
                )
            )

        if pending:
            session.add_all(pending)
            session.commit()
    finally:
        session.close()


def get_db_session_from_factory(session_factory: sessionmaker[Session]) -> Generator[Session, None, None]:
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
