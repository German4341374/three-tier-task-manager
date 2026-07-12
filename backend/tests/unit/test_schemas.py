import pytest
from pydantic import ValidationError

from app.schemas import TaskCreate, TaskUpdate


def test_task_create_trims_no_data_implicitly() -> None:
    task = TaskCreate(title="Document deployment", description=None)
    assert task.title == "Document deployment"


def test_task_create_rejects_empty_title() -> None:
    with pytest.raises(ValidationError):
        TaskCreate(title="")


def test_task_update_tracks_only_supplied_fields() -> None:
    update = TaskUpdate(completed=True)
    assert update.model_dump(exclude_unset=True) == {"completed": True}
