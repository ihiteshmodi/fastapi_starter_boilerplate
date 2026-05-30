from pathlib import Path

from alembic import command
from alembic.config import Config


def run_migrations(database_url: str) -> None:
    project_root = Path(__file__).resolve().parents[2]
    alembic_ini = project_root / "alembic.ini"

    alembic_cfg = Config(str(alembic_ini))
    alembic_cfg.set_main_option("script_location", str(project_root / "alembic"))
    alembic_cfg.set_main_option("sqlalchemy.url", database_url)
    command.upgrade(alembic_cfg, "head")
