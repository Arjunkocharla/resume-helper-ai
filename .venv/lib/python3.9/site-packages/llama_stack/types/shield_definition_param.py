# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypedDict

from .tool_param_definition_param import ToolParamDefinitionParam
from .rest_api_execution_config_param import RestAPIExecutionConfigParam

__all__ = ["ShieldDefinitionParam"]


class ShieldDefinitionParam(TypedDict, total=False):
    on_violation_action: Required[Literal[0, 1, 2]]

    shield_type: Required[
        Union[
            Literal["llama_guard", "code_scanner_guard", "third_party_shield", "injection_shield", "jailbreak_shield"],
            str,
        ]
    ]

    description: str

    execution_config: RestAPIExecutionConfigParam

    parameters: Dict[str, ToolParamDefinitionParam]
