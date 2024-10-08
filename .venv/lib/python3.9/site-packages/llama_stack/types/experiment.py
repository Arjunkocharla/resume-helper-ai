# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Experiment"]


class Experiment(BaseModel):
    id: str

    created_at: datetime

    metadata: Dict[str, Union[bool, float, str, List[object], object, None]]

    name: str

    status: Literal["not_started", "running", "completed", "failed"]

    updated_at: datetime
