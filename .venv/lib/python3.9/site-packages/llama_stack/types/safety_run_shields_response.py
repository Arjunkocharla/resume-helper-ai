# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .sheid_response import SheidResponse

__all__ = ["SafetyRunShieldsResponse"]


class SafetyRunShieldsResponse(BaseModel):
    responses: List[SheidResponse]
