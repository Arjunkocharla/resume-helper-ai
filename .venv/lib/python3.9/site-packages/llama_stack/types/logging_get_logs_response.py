# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union
from datetime import datetime

from .._models import BaseModel

__all__ = ["LoggingGetLogsResponse"]


class LoggingGetLogsResponse(BaseModel):
    additional_info: Dict[str, Union[bool, float, str, List[object], object, None]]

    level: str

    message: str

    timestamp: datetime
