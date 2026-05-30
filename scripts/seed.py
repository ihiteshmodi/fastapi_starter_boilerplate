import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.config import get_settings
from app.services.migrations import run_migrations
from app.services.memory_service import create_session_factory, seed_demo_users


def main() -> None:
    settings = get_settings()
    run_migrations(settings.database_url)
    session_factory = create_session_factory(settings.database_url)
    seed_demo_users(
        session_factory,
        basic_username=settings.basic_username,
        basic_password=settings.basic_password,
        premium_username=settings.premium_username,
        premium_password=settings.premium_password,
        salt=settings.auth_password_salt,
    )
    print("Seeded demo users")


if __name__ == "__main__":
    main()
