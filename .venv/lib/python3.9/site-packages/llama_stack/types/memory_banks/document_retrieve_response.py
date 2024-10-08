# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union

from ..._models import BaseModel

__all__ = ["DocumentRetrieveResponse"]


class DocumentRetrieveResponse(BaseModel):
    content: Union[str, List[str]]

    document_id: str

    metadata: Dict[str, Union[bool, float, str, List[object], object, None]]

    mime_type: str
