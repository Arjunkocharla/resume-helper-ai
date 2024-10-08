# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Required, TypedDict

__all__ = ["LoggingGetLogsParams", "Request"]


class LoggingGetLogsParams(TypedDict, total=False):
    request: Required[Request]


class Request(TypedDict, total=False):
    query: Required[str]

    filters: Dict[str, Union[bool, float, str, Iterable[object], object, None]]
