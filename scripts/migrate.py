from app.config import get_settings
from app.services.memory_service import create_session_factory


def main() -> None:
    settings = get_settings()
    create_session_factory(settings.database_url)
    print("Database schema initialized")


if __name__ == "__main__":
    main()
