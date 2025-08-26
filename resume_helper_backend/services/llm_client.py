#!/usr/bin/env python3
"""Unified LLM Client for multiple providers"""

import logging
import json
import time
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod

from config.llm_config import LLMProvider, llm_config

logger = logging.getLogger(__name__)

class BaseLLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    def create_message(self, model: str, messages: List[Dict], system: Optional[str] = None, **kwargs) -> Dict:
        """Create a message completion"""
        pass
    
    @abstractmethod
    def get_model_name(self, quality: str = 'fast') -> str:
        """Get the model name for this provider"""
        pass

class AnthropicClient(BaseLLMClient):
    """Anthropic Claude client"""
    
    def __init__(self):
        from anthropic import Anthropic
        config = llm_config.get_provider_config(LLMProvider.ANTHROPIC)
        self.client = Anthropic(api_key=config['api_key'])
        self.provider = LLMProvider.ANTHROPIC
    
    def create_message(self, model: str, messages: List[Dict], system: Optional[str] = None, **kwargs) -> Dict:
        """Create a message using Anthropic's API"""
        try:
            # Convert OpenAI format to Anthropic format
            if system:
                system_prompt = system
            else:
                system_prompt = "You are a helpful AI assistant."
            
            # Extract user message from messages
            user_message = None
            for msg in messages:
                if msg.get('role') == 'user':
                    user_message = msg.get('content', '')
                    break
            
            if not user_message:
                raise ValueError("No user message found in messages")
            
            response = self.client.messages.create(
                model=model,
                max_tokens=kwargs.get('max_tokens', 1000),
                temperature=kwargs.get('temperature', 0.1),
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}]
            )
            
            return {
                'content': response.content[0].text,
                'usage': {
                    'prompt_tokens': response.usage.input_tokens,
                    'completion_tokens': response.usage.output_tokens,
                    'total_tokens': response.usage.input_tokens + response.usage.output_tokens
                },
                'provider': 'anthropic'
            }
            
        except Exception as e:
            logger.error(f"Anthropic API call failed: {e}")
            raise
    
    def get_model_name(self, quality: str = 'fast') -> str:
        """Get Anthropic model name"""
        return llm_config.get_model_name(LLMProvider.ANTHROPIC, quality)

class GroqClient(BaseLLMClient):
    """Groq client using OpenAI-compatible API"""
    
    def __init__(self):
        import openai
        config = llm_config.get_provider_config(LLMProvider.GROQ)
        
        # Configure OpenAI client for Groq
        self.client = openai.OpenAI(
            api_key=config['api_key'],
            base_url=config['base_url']
        )
        self.provider = LLMProvider.GROQ
    
    def create_message(self, model: str, messages: List[Dict], system: Optional[str] = None, **kwargs) -> Dict:
        """Create a message using Groq's OpenAI-compatible API"""
        try:
            # Add system message if provided
            if system:
                messages = [{"role": "system", "content": system}] + messages
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=kwargs.get('max_tokens', 1000),
                temperature=kwargs.get('temperature', 0.1)
            )
            
            return {
                'content': response.choices[0].message.content,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                },
                'provider': 'groq'
            }
            
        except Exception as e:
            logger.error(f"Groq API call failed: {e}")
            raise
    
    def get_model_name(self, quality: str = 'fast') -> str:
        """Get Groq model name"""
        return llm_config.get_model_name(LLMProvider.GROQ, quality)

class GPT5NanoClient(BaseLLMClient):
    """OpenAI client for GPT-5 Nano models"""
    
    def __init__(self):
        import openai
        config = llm_config.get_provider_config(LLMProvider.GPT5_NANO)
        
        # Configure OpenAI client
        self.client = openai.OpenAI(
            api_key=config['api_key'],
            base_url=config['base_url']
        )
        self.provider = LLMProvider.GPT5_NANO
    
    def create_message(self, model: str, messages: List[Dict], system: Optional[str] = None, **kwargs) -> Dict:
        """Create a message using OpenAI's API for GPT-5 Nano"""
        try:
            if system:
                messages = [{"role": "system", "content": system}] + messages
            
            # GPT-5 Nano: use minimal supported params (model, messages). No temperature/max tokens.
            resp = self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            content = resp.choices[0].message.content
            usage = getattr(resp, 'usage', None)
            return {
                'content': content,
                'usage': {
                    'prompt_tokens': getattr(usage, 'prompt_tokens', None),
                    'completion_tokens': getattr(usage, 'completion_tokens', None),
                    'total_tokens': getattr(usage, 'total_tokens', None)
                },
                'provider': 'gpt5_nano'
            }
        except Exception as e:
            logger.error(f"GPT-5 Nano API call failed: {e}")
            raise
    
    def get_model_name(self, quality: str = 'fast') -> str:
        return llm_config.get_model_name(LLMProvider.GPT5_NANO, quality)

class UnifiedLLMClient:
    """Unified client that can switch between LLM providers"""
    
    def __init__(self, preferred_provider: Optional[LLMProvider] = None):
        # Default to Groq for cost savings, unless explicitly specified
        if preferred_provider is None:
            self.preferred_provider = LLMProvider.GROQ  # Always prefer Groq
        else:
            self.preferred_provider = preferred_provider
        
        logger.info(f"UnifiedLLMClient initialized with preferred provider: {self.preferred_provider.value}")
        self.clients = {}
        self._initialize_clients()
        self.last_groq_call = 0  # Track last Groq call time for rate limiting
    
    def _initialize_clients(self):
        """Initialize available LLM clients"""
        try:
            if llm_config.providers[LLMProvider.ANTHROPIC]['enabled']:
                self.clients[LLMProvider.ANTHROPIC] = AnthropicClient()
                logger.info("Anthropic client initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Anthropic client: {e}")
        
        try:
            if llm_config.providers[LLMProvider.GROQ]['enabled']:
                self.clients[LLMProvider.GROQ] = GroqClient()
                logger.info("Groq client initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Groq client: {e}")

        try:
            if llm_config.providers.get(LLMProvider.GPT5_NANO, {}).get('enabled'):
                self.clients[LLMProvider.GPT5_NANO] = GPT5NanoClient()
                logger.info("GPT-5 Nano client initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize GPT-5 Nano client: {e}")
        
        if not self.clients:
            raise ValueError("No LLM clients could be initialized")
    
    def create_message(self, 
                      provider: Optional[LLMProvider] = None,
                      quality: str = 'fast',
                      messages: List[Dict] = None,
                      system: Optional[str] = None,
                      **kwargs) -> Dict:
        """
        Create a message using the specified or preferred provider
        
        Args:
            provider: Specific provider to use (None = use preferred)
            quality: Model quality ('fast', 'balanced', 'powerful')
            messages: List of message dictionaries
            system: Optional system prompt
            **kwargs: Additional parameters for the LLM call
        """
        # Determine which provider to use
        target_provider = provider or self.preferred_provider
        
        # Try preferred provider first
        if target_provider in self.clients:
            try:
                client = self.clients[target_provider]
                model = client.get_model_name(quality)
                
                # Add rate limiting for Groq (100 requests/minute = 1 request every 0.6 seconds)
                if target_provider == LLMProvider.GROQ:
                    current_time = time.time()
                    time_since_last_call = current_time - self.last_groq_call
                    if time_since_last_call < 0.6:  # Less than 0.6 seconds since last call
                        sleep_time = 0.6 - time_since_last_call
                        logger.info(f"Rate limiting: waiting {sleep_time:.2f}s before Groq call")
                        time.sleep(sleep_time)
                    self.last_groq_call = time.time()
                
                logger.info(f"Using {target_provider.value} with model {model}")
                
                result = client.create_message(model, messages, system, **kwargs)
                result['provider_used'] = target_provider.value
                return result
                
            except Exception as e:
                # Check if it's a rate limit error - immediately fallback
                if "429" in str(e) or "Too Many Requests" in str(e):
                    logger.warning(f"{target_provider.value} hit rate limit, immediately falling back")
                else:
                    logger.warning(f"{target_provider.value} failed: {e}")
        
        # Fallback to any available provider
        for fallback_provider, client in self.clients.items():
            if fallback_provider != target_provider:
                try:
                    model = client.get_model_name(quality)
                    logger.info(f"Fallback to {fallback_provider.value} with model {model}")
                    
                    result = client.create_message(model, messages, system, **kwargs)
                    result['provider_used'] = fallback_provider.value
                    result['fallback'] = True
                    return result
                    
                except Exception as e:
                    logger.warning(f"Fallback to {fallback_provider.value} failed: {e}")
        
        raise RuntimeError("All LLM providers failed")
    
    def get_available_providers(self) -> List[str]:
        """Get list of available provider names"""
        return [provider.value for provider in self.clients.keys()]
    
    def get_cost_estimate(self, provider: LLMProvider, token_count: int) -> float:
        """Get cost estimate for a provider"""
        return llm_config.get_cost_estimate(provider, token_count)
