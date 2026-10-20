
from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from recall.models import MemoryOperation, MemoryRecord


def test_memory_record_stores_identity_and_content():
    record = MemoryRecord(
        id="mem-1",
        user_id="user-1",
        content="I prefer Python.",
    )

    assert record.id == "mem-1"
    assert record.user_id == "user-1"
    assert record.content == "I prefer Python."
    assert record.source_type == "text"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", ""),
        ("id", "   "),
        ("user_id", ""),
        ("user_id", "   "),
        ("content", ""),
        ("content", "   "),
    ],
)
def test_memory_record_rejects_empty_required_values(field, value):
    fields = {
        "id": "mem-1",
        "user_id": "user-1",
        "content": "A valid memory.",
    }
    fields[field] = value

    with pytest.raises(ValidationError):
        MemoryRecord(**fields)


def test_memory_record_has_creation_timestamp():
    before = datetime.now(UTC)
    record = MemoryRecord(
        id="mem-1",
        user_id="user-1",
        content="I prefer Python.",
    )
    after = datetime.now(UTC)

    assert before <= record.created_at <= after
    assert record.created_at.tzinfo is not None


def test_memory_record_supports_multimodal_provenance():
    record = MemoryRecord(
        id="mem-1",
        user_id="user-1",
        content="My dog is named Milo.",
        source_type="audio",
        metadata={"filename": "conversation.wav"},
    )

    assert record.source_type == "audio"
    assert record.metadata["filename"] == "conversation.wav"


@pytest.mark.parametrize("source_type", ["text", "document", "image", "audio"])
def test_memory_record_accepts_supported_source_types(source_type):
    record = MemoryRecord(
        id="mem-1",
        user_id="user-1",
        content="A memory.",
        source_type=source_type,
    )

    assert record.source_type == source_type


def test_memory_record_rejects_unknown_source_type():
    with pytest.raises(ValidationError):
        MemoryRecord(
            id="mem-1",
            user_id="user-1",
            content="A memory.",
            source_type="video",
        )


def test_memory_record_rejects_unexpected_fields():
    with pytest.raises(ValidationError):
        MemoryRecord(
            id="mem-1",
            user_id="user-1",
            content="A memory.",
            unknown_field="unexpected",
        )


def test_memory_record_metadata_defaults_are_independent():
    first = MemoryRecord(id="mem-1", user_id="user-1", content="First memory.")
    second = MemoryRecord(id="mem-2", user_id="user-1", content="Second memory.")

    first.metadata["tag"] = "personal"

    assert second.metadata == {}


@pytest.mark.parametrize(
    ("operation", "fields"),
    [
        ("ADD", {"content": "I prefer Python."}),
        ("UPDATE", {"memory_id": "mem-1", "content": "I prefer Rust."}),
        ("DELETE", {"memory_id": "mem-1"}),
        ("NONE", {}),
    ],
)
def test_memory_operation_accepts_valid_actions(operation, fields):
    result = MemoryOperation(operation=operation, **fields)

    assert result.operation == operation


def test_memory_operation_rejects_unknown_action():
    with pytest.raises(ValidationError):
        MemoryOperation(operation="MERGE")


@pytest.mark.parametrize(
    ("operation", "fields"),
    [
        ("ADD", {}),
        ("ADD", {"content": "New fact", "memory_id": "mem-1"}),
        ("UPDATE", {"memory_id": "mem-1"}),
        ("UPDATE", {"content": "Replacement fact"}),
        ("DELETE", {}),
        ("DELETE", {"memory_id": "mem-1", "content": "Unexpected content"}),
        ("NONE", {"memory_id": "mem-1"}),
        ("NONE", {"content": "Unexpected content"}),
    ],
)
def test_memory_operation_rejects_invalid_field_combinations(operation, fields):
    with pytest.raises(ValidationError):
        MemoryOperation(operation=operation, **fields)


@pytest.mark.parametrize(
    ("memory_id", "content"),
    [
        ("   ", "Updated fact"),
        ("mem-1", "   "),
    ],
)
def test_memory_operation_rejects_whitespace_only_values(memory_id, content):
    with pytest.raises(ValidationError):
        MemoryOperation(
            operation="UPDATE",
            memory_id=memory_id,
            content=content,
        )


def test_memory_operation_rejects_unexpected_fields():
    with pytest.raises(ValidationError):
        MemoryOperation(
            operation="ADD",
            content="A new fact.",
            extra_field="unexpected",
        )
