# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["Run"]


class Run(BaseModel):
    id: str

    experiment_id: str

    metadata: Dict[str, Union[bool, float, str, List[object], object, None]]

    started_at: datetime

    status: str

    ended_at: Optional[datetime] = None
