# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..types import safety_run_shields_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.shield_definition_param import ShieldDefinitionParam
from ..types.safety_run_shields_response import SafetyRunShieldsResponse

__all__ = ["SafetyResource", "AsyncSafetyResource"]


class SafetyResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SafetyResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#accessing-raw-response-data-eg-headers
        """
        return SafetyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SafetyResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#with_streaming_response
        """
        return SafetyResourceWithStreamingResponse(self)

    def run_shields(
        self,
        *,
        messages: Iterable[safety_run_shields_params.Message],
        shields: Iterable[ShieldDefinitionParam],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SafetyRunShieldsResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/safety/run_shields",
            body=maybe_transform(
                {
                    "messages": messages,
                    "shields": shields,
                },
                safety_run_shields_params.SafetyRunShieldsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SafetyRunShieldsResponse,
        )


class AsyncSafetyResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSafetyResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSafetyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSafetyResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/llama-stack-python#with_streaming_response
        """
        return AsyncSafetyResourceWithStreamingResponse(self)

    async def run_shields(
        self,
        *,
        messages: Iterable[safety_run_shields_params.Message],
        shields: Iterable[ShieldDefinitionParam],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SafetyRunShieldsResponse:
        """
        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/safety/run_shields",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "shields": shields,
                },
                safety_run_shields_params.SafetyRunShieldsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SafetyRunShieldsResponse,
        )


class SafetyResourceWithRawResponse:
    def __init__(self, safety: SafetyResource) -> None:
        self._safety = safety

        self.run_shields = to_raw_response_wrapper(
            safety.run_shields,
        )


class AsyncSafetyResourceWithRawResponse:
    def __init__(self, safety: AsyncSafetyResource) -> None:
        self._safety = safety

        self.run_shields = async_to_raw_response_wrapper(
            safety.run_shields,
        )


class SafetyResourceWithStreamingResponse:
    def __init__(self, safety: SafetyResource) -> None:
        self._safety = safety

        self.run_shields = to_streamed_response_wrapper(
            safety.run_shields,
        )


class AsyncSafetyResourceWithStreamingResponse:
    def __init__(self, safety: AsyncSafetyResource) -> None:
        self._safety = safety

        self.run_shields = async_to_streamed_response_wrapper(
            safety.run_shields,
        )
