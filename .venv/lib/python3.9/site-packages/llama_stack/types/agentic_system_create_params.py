# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .shield_definition_param import ShieldDefinitionParam
from .tool_param_definition_param import ToolParamDefinitionParam
from .shared_params.sampling_params import SamplingParams
from .rest_api_execution_config_param import RestAPIExecutionConfigParam

__all__ = [
    "AgenticSystemCreateParams",
    "AgentConfig",
    "AgentConfigTool",
    "AgentConfigToolSearchToolDefinition",
    "AgentConfigToolWolframAlphaToolDefinition",
    "AgentConfigToolPhotogenToolDefinition",
    "AgentConfigToolCodeInterpreterToolDefinition",
    "AgentConfigToolFunctionCallToolDefinition",
    "AgentConfigToolUnionMember5",
    "AgentConfigToolUnionMember5MemoryBankConfig",
    "AgentConfigToolUnionMember5MemoryBankConfigUnionMember0",
    "AgentConfigToolUnionMember5MemoryBankConfigUnionMember1",
    "AgentConfigToolUnionMember5MemoryBankConfigUnionMember2",
    "AgentConfigToolUnionMember5MemoryBankConfigUnionMember3",
    "AgentConfigToolUnionMember5QueryGeneratorConfig",
    "AgentConfigToolUnionMember5QueryGeneratorConfigUnionMember0",
    "AgentConfigToolUnionMember5QueryGeneratorConfigUnionMember1",
    "AgentConfigToolUnionMember5QueryGeneratorConfigType",
]


class AgenticSystemCreateParams(TypedDict, total=False):
    agent_config: Required[AgentConfig]


class AgentConfigToolSearchToolDefinition(TypedDict, total=False):
    engine: Required[Literal["bing", "brave"]]

    type: Required[Literal["brave_search"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    remote_execution: RestAPIExecutionConfigParam


class AgentConfigToolWolframAlphaToolDefinition(TypedDict, total=False):
    type: Required[Literal["wolfram_alpha"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    remote_execution: RestAPIExecutionConfigParam


class AgentConfigToolPhotogenToolDefinition(TypedDict, total=False):
    type: Required[Literal["photogen"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    remote_execution: RestAPIExecutionConfigParam


class AgentConfigToolCodeInterpreterToolDefinition(TypedDict, total=False):
    enable_inline_code_execution: Required[bool]

    type: Required[Literal["code_interpreter"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    remote_execution: RestAPIExecutionConfigParam


class AgentConfigToolFunctionCallToolDefinition(TypedDict, total=False):
    description: Required[str]

    function_name: Required[str]

    parameters: Required[Dict[str, ToolParamDefinitionParam]]

    type: Required[Literal["function_call"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    remote_execution: RestAPIExecutionConfigParam


class AgentConfigToolUnionMember5MemoryBankConfigUnionMember0(TypedDict, total=False):
    bank_id: Required[str]

    type: Required[Literal["vector"]]


class AgentConfigToolUnionMember5MemoryBankConfigUnionMember1(TypedDict, total=False):
    bank_id: Required[str]

    keys: Required[List[str]]

    type: Required[Literal["keyvalue"]]


class AgentConfigToolUnionMember5MemoryBankConfigUnionMember2(TypedDict, total=False):
    bank_id: Required[str]

    type: Required[Literal["keyword"]]


class AgentConfigToolUnionMember5MemoryBankConfigUnionMember3(TypedDict, total=False):
    bank_id: Required[str]

    entities: Required[List[str]]

    type: Required[Literal["graph"]]


AgentConfigToolUnionMember5MemoryBankConfig: TypeAlias = Union[
    AgentConfigToolUnionMember5MemoryBankConfigUnionMember0,
    AgentConfigToolUnionMember5MemoryBankConfigUnionMember1,
    AgentConfigToolUnionMember5MemoryBankConfigUnionMember2,
    AgentConfigToolUnionMember5MemoryBankConfigUnionMember3,
]


class AgentConfigToolUnionMember5QueryGeneratorConfigUnionMember0(TypedDict, total=False):
    sep: Required[str]

    type: Required[Literal["default"]]


class AgentConfigToolUnionMember5QueryGeneratorConfigUnionMember1(TypedDict, total=False):
    model: Required[str]

    template: Required[str]

    type: Required[Literal["llm"]]


class AgentConfigToolUnionMember5QueryGeneratorConfigType(TypedDict, total=False):
    type: Required[Literal["custom"]]


AgentConfigToolUnionMember5QueryGeneratorConfig: TypeAlias = Union[
    AgentConfigToolUnionMember5QueryGeneratorConfigUnionMember0,
    AgentConfigToolUnionMember5QueryGeneratorConfigUnionMember1,
    AgentConfigToolUnionMember5QueryGeneratorConfigType,
]


class AgentConfigToolUnionMember5(TypedDict, total=False):
    max_chunks: Required[int]

    max_tokens_in_context: Required[int]

    memory_bank_configs: Required[Iterable[AgentConfigToolUnionMember5MemoryBankConfig]]

    query_generator_config: Required[AgentConfigToolUnionMember5QueryGeneratorConfig]

    type: Required[Literal["memory"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]


AgentConfigTool: TypeAlias = Union[
    AgentConfigToolSearchToolDefinition,
    AgentConfigToolWolframAlphaToolDefinition,
    AgentConfigToolPhotogenToolDefinition,
    AgentConfigToolCodeInterpreterToolDefinition,
    AgentConfigToolFunctionCallToolDefinition,
    AgentConfigToolUnionMember5,
]


class AgentConfig(TypedDict, total=False):
    instructions: Required[str]

    model: Required[str]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    sampling_params: SamplingParams

    tool_choice: Literal["auto", "required"]

    tool_prompt_format: Literal["json", "function_tag"]
    """
    `json` -- Refers to the json format for calling tools. The json format takes the
    form like { "type": "function", "function" : { "name": "function_name",
    "description": "function_description", "parameters": {...} } }

    `function_tag` -- This is an example of how you could define your own user
    defined format for making tool calls. The function_tag format looks like this,
    <function=function_name>(parameters)</function>

    The detailed prompts for each of these formats are added to llama cli
    """

    tools: Iterable[AgentConfigTool]
