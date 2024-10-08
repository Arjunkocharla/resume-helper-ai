# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union

from ..._models import BaseModel

__all__ = ["Attachment"]


class Attachment(BaseModel):
    content: Union[str, List[str]]

    mime_type: str
