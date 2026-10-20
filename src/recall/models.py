
"""Core domain models for Recall."""

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


SourceType = Literal["text", "document", "image", "audio"]
OperationType = Literal["ADD", "UPDATE", "DELETE", "NONE"]


class MemoryRecord(BaseModel):
    """A single memory belonging to a specific user."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source_type: SourceType = "text"
    metadata: dict[str, str | int | float | bool | None] = Field(
        default_factory=dict
    )

    @field_validator("id", "user_id")
    @classmethod
    def validate_identifiers(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Must not be empty or whitespace")
        return value

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Content must not be empty or whitespace")
        return value


class MemoryOperation(BaseModel):
    """A proposed change to the memory store."""

    model_config = ConfigDict(extra="forbid")

    operation: OperationType
    memory_id: str | None = None
    content: str | None = None

    @field_validator("memory_id")
    @classmethod
    def validate_memory_id(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("memory_id must not be empty or whitespace")
        return value

    @field_validator("content")
    @classmethod
    def validate_operation_content(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("content must not be empty or whitespace")
        return value

    @model_validator(mode="after")
    def validate_operation_fields(self) -> "MemoryOperation":
        if self.operation == "ADD":
            if self.content is None:
                raise ValueError("ADD requires content")
            if self.memory_id is not None:
                raise ValueError("ADD must not specify memory_id")

        elif self.operation == "UPDATE":
            if self.memory_id is None or self.content is None:
                raise ValueError("UPDATE requires memory_id and content")

        elif self.operation == "DELETE":
            if self.memory_id is None:
                raise ValueError("DELETE requires memory_id")
            if self.content is not None:
                raise ValueError("DELETE must not specify content")

        elif self.operation == "NONE":
            if self.memory_id is not None or self.content is not None:
                raise ValueError("NONE must not specify memory_id or content")

        return self
