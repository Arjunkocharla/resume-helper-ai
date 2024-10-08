# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["RunUpdateParams", "Request"]


class RunUpdateParams(TypedDict, total=False):
    request: Required[Request]


class Request(TypedDict, total=False):
    run_id: Required[str]

    ended_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    metadata: Dict[str, Union[bool, float, str, Iterable[object], object, None]]

    status: str
