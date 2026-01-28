"""
Configuration settings for AI Data Engineer Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # LLM Provider
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    
    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
    
    # Embedding Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # Vector Store Configuration
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
    
    # Application Settings
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "200"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Agent Prompts
    SQL_AGENT_PROMPT = """You are an expert SQL developer. Generate SQL queries based on the user's question and the provided schema context.
    Always explain your query and include comments."""
    
    QUALITY_AGENT_PROMPT = """You are a data quality expert. Analyze the schema and suggest comprehensive data quality rules.
    Include null checks, range validations, format checks, and referential integrity rules."""
    
    SPARK_AGENT_PROMPT = """You are a Spark optimization expert. Analyze the data processing requirements and suggest optimization techniques.
    Include partitioning strategies, caching recommendations, and performance tuning tips."""
    
    DEPENDENCY_AGENT_PROMPT = """You are a data architecture expert. Analyze table relationships and identify dependencies.
    Suggest join strategies and create dependency graphs."""
    
    DOCUMENTATION_AGENT_PROMPT = """You are a technical documentation expert. Generate comprehensive documentation for the dataset.
    Include data dictionary, schema descriptions, and usage examples."""

settings = Settings()
