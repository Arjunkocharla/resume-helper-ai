# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["UserMessage"]


class UserMessage(BaseModel):
    content: Union[str, List[str]]

    role: Literal["user"]

    context: Union[str, List[str], None] = None
