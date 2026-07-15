from pathlib import Path

from alembic.config import Config


BACKEND_ROOT = Path(__file__).resolve().parents[1]


def test_alembic_configuration_targets_backend_metadata():
    config_path = BACKEND_ROOT / "alembic.ini"
    assert config_path.is_file()

    config = Config(str(config_path))
    assert config.get_main_option("script_location") == "alembic"
    assert (BACKEND_ROOT / "alembic" / "env.py").is_file()


def test_initial_revision_exists():
    versions = BACKEND_ROOT / "alembic" / "versions"
    revisions = list(versions.glob("*.py"))
    assert revisions, "at least one Alembic revision must define the schema baseline"
