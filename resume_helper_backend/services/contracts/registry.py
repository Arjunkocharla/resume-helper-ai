from typing import Any, Type, TypeVar

from pydantic import BaseModel


SCHEMA_VERSION: str = "v1"

T = TypeVar("T", bound=BaseModel)


def to_json(model: BaseModel) -> str:
    """Serialize a Pydantic model to JSON string using v2 API."""
    return model.model_dump_json()


def from_json(model_cls: Type[T], json_str: str) -> T:
    """Deserialize JSON string to a Pydantic model using v2 API."""
    return model_cls.model_validate_json(json_str)


def validate_or_raise(model_cls: Type[T], data: Any) -> T:
    """Validate arbitrary data into a Pydantic model, raising on error."""
    return model_cls.model_validate(data)


