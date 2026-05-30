import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.config import get_settings
from app.services.migrations import run_migrations


def main() -> None:
    settings = get_settings()
    run_migrations(settings.database_url)
    print("Alembic migrations applied")


if __name__ == "__main__":
    main()
