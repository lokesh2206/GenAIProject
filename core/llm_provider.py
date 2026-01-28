"""
LLM Provider Module - Abstract interface for multiple LLM providers
"""
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain.schema import HumanMessage, SystemMessage
from config.settings import settings

class LLMProvider:
    """Abstract LLM provider supporting OpenAI, Llama, and Mistral"""
    
    def __init__(self, provider: str = None, model: str = None, temperature: float = None):
        """
        Initialize LLM provider
        
        Args:
            provider: LLM provider name (openai, llama, mistral)
            model: Model name
            temperature: Temperature for generation
        """
        self.provider = provider or settings.LLM_PROVIDER
        self.temperature = temperature or settings.TEMPERATURE
        self.llm = None
        
        # Set model based on provider
        if self.provider == "openai":
            self.model = model or settings.OPENAI_MODEL
        elif self.provider in ["llama", "mistral"]:
            self.model = model or settings.OLLAMA_MODEL
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
        
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the LLM based on provider"""
        try:
            if self.provider == "openai":
                self._initialize_openai()
            elif self.provider in ["llama", "mistral"]:
                self._initialize_ollama()
        except Exception as e:
            raise Exception(f"Error initializing LLM provider: {str(e)}")
    
    def _initialize_openai(self):
        """Initialize OpenAI LLM"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in environment variables")
        
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            openai_api_key=settings.OPENAI_API_KEY
        )
        print(f"Initialized OpenAI LLM: {self.model}")
    
    def _initialize_ollama(self):
        """Initialize Ollama LLM (for Llama/Mistral)"""
        self.llm = Ollama(
            model=self.model,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=self.temperature
        )
        print(f"Initialized Ollama LLM: {self.model}")
    
    def generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate response from LLM
        
        Args:
            prompt: User prompt
            system_message: Optional system message
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            if self.provider == "openai":
                return self._generate_openai(prompt, system_message, max_tokens)
            else:
                return self._generate_ollama(prompt, system_message)
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
    
    def _generate_openai(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate response using OpenAI"""
        messages = []
        
        if system_message:
            messages.append(SystemMessage(content=system_message))
        
        messages.append(HumanMessage(content=prompt))
        
        kwargs = {}
        if max_tokens:
            kwargs['max_tokens'] = max_tokens
        
        response = self.llm.invoke(messages, **kwargs)
        return response.content
    
    def _generate_ollama(
        self,
        prompt: str,
        system_message: Optional[str] = None
    ) -> str:
        """Generate response using Ollama"""
        full_prompt = prompt
        
        if system_message:
            full_prompt = f"{system_message}\n\n{prompt}"
        
        response = self.llm.invoke(full_prompt)
        return response
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about the current provider"""
        return {
            "provider": self.provider,
            "model": self.model,
            "temperature": self.temperature
        }
