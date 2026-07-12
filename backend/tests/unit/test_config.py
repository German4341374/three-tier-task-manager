import pytest
from pydantic import ValidationError

from app.config import Settings


def test_settings_parse_allowed_hosts() -> None:
    settings = Settings(
        database_url="postgresql://user:pass@db:5432/tasks",
        allowed_hosts="localhost, tasks.example.test",
    )
    assert settings.allowed_hosts_list == ["localhost", "tasks.example.test"]


def test_settings_reject_invalid_environment() -> None:
    with pytest.raises(ValidationError):
        Settings(database_url="postgresql://user:pass@db/tasks", environment="staging")
