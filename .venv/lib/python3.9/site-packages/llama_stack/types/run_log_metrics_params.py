# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["RunLogMetricsParams", "Request", "RequestMetric"]


class RunLogMetricsParams(TypedDict, total=False):
    request: Required[Request]


class RequestMetric(TypedDict, total=False):
    name: Required[str]

    run_id: Required[str]

    timestamp: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    value: Required[Union[float, str, bool]]


class Request(TypedDict, total=False):
    metrics: Required[Iterable[RequestMetric]]

    run_id: Required[str]
