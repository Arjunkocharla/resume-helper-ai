#!/usr/bin/env python3
"""LLM Configuration and Provider Management"""

import os
import logging
from typing import Dict, Optional, Any
from enum import Enum

logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    """Available LLM providers"""
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    OPENAI = "openai"
    GPT5_NANO = "gpt5_nano"

class LLMConfig:
    """Configuration manager for different LLM providers"""
    
    def __init__(self):
        self.providers = {
            LLMProvider.ANTHROPIC: {
                'api_key': os.getenv('ANTHROPIC_API_KEY'),
                'base_url': 'https://api.anthropic.com',
                'models': {
                    'fast': 'claude-3-haiku-20240307',
                    'balanced': 'claude-3-sonnet-20240229',
                    'powerful': 'claude-3-opus-20240229'
                },
                'cost_per_1m_tokens': 0.25,
                'enabled': bool(os.getenv('ANTHROPIC_API_KEY'))
            },
            LLMProvider.GROQ: {
                'api_key': os.getenv('GROQ_API_KEY'),
                'base_url': 'https://api.groq.com/openai/v1',
                'models': {
                    'fast': 'llama3-8b-8192',
                    'balanced': 'llama3-70b-8192',
                    'powerful': 'mixtral-8x7b-32768'
                },
                'cost_per_1m_tokens': 0.05,
                'enabled': bool(os.getenv('GROQ_API_KEY'))
            },
            # GPT-5 Nano via OpenAI API
            LLMProvider.GPT5_NANO: {
                'api_key': os.getenv('OPENAI_API_KEY'),
                'base_url': os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
                'models': {
                    'fast': 'gpt-5-nano',
                    'balanced': 'gpt-5-nano',
                    'powerful': 'gpt-5-nano'
                },
                # Note: pricing here is simplified (input $0.05/M, output $0.40/M). We track one figure for display.
                'cost_per_1m_tokens': 0.05,
                'enabled': bool(os.getenv('OPENAI_API_KEY'))
            }
        }
        
        # Set default provider based on availability and cost
        self.default_provider = self._get_default_provider()
        logger.info(f"Default LLM provider: {self.default_provider}")
    
    def _get_default_provider(self) -> LLMProvider:
        """Get the best default provider based on availability and cost"""
        # Always prefer Groq as default (cheapest), even if not configured
        # The client will handle fallback when making actual API calls
        return LLMProvider.GROQ
    
    def get_provider_config(self, provider: LLMProvider) -> Dict[str, Any]:
        """Get configuration for a specific provider"""
        if provider not in self.providers:
            raise ValueError(f"Provider {provider} not configured")
        
        config = self.providers[provider]
        if not config['enabled']:
            raise ValueError(f"Provider {provider} is not enabled (missing API key)")
        
        return config
    
    def get_model_name(self, provider: LLMProvider, quality: str = 'fast') -> str:
        """Get model name for a provider and quality level"""
        config = self.get_provider_config(provider)
        return config['models'].get(quality, config['models']['fast'])
    
    def get_cost_estimate(self, provider: LLMProvider, token_count: int) -> float:
        """Estimate cost for a given token count"""
        config = self.get_provider_config(provider)
        return (token_count / 1_000_000) * config['cost_per_1m_tokens']
    
    def list_available_providers(self) -> Dict[str, Dict]:
        """List all available providers with their status"""
        # Check current environment variables dynamically
        return {
            provider.value: {
                'enabled': bool(os.getenv('ANTHROPIC_API_KEY') if provider == LLMProvider.ANTHROPIC else os.getenv('GROQ_API_KEY')),
                'cost_per_1m_tokens': config['cost_per_1m_tokens'],
                'models': list(config['models'].keys())
            }
            for provider, config in self.providers.items()
        }

# Global instance
llm_config = LLMConfig()
