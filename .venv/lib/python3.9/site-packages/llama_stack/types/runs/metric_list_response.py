# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from datetime import datetime

from ..._models import BaseModel

__all__ = ["MetricListResponse"]


class MetricListResponse(BaseModel):
    name: str

    run_id: str

    timestamp: datetime

    value: Union[float, str, bool]
