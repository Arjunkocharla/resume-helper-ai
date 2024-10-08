# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["LoggingLogMessagesParams", "Request", "RequestLog"]


class LoggingLogMessagesParams(TypedDict, total=False):
    request: Required[Request]


class RequestLog(TypedDict, total=False):
    additional_info: Required[Dict[str, Union[bool, float, str, Iterable[object], object, None]]]

    level: Required[str]

    message: Required[str]

    timestamp: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]


class Request(TypedDict, total=False):
    logs: Required[Iterable[RequestLog]]

    run_id: str
