# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ToolResponseMessage"]


class ToolResponseMessage(BaseModel):
    call_id: str

    content: Union[str, List[str]]

    role: Literal["ipython"]

    tool_name: Union[Literal["brave_search", "wolfram_alpha", "photogen", "code_interpreter"], str]
