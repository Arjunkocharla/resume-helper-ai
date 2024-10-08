# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["SheidResponse"]


class SheidResponse(BaseModel):
    is_violation: bool

    shield_type: Union[
        Literal["llama_guard", "code_scanner_guard", "third_party_shield", "injection_shield", "jailbreak_shield"], str
    ]

    violation_return_message: Optional[str] = None

    violation_type: Optional[str] = None
