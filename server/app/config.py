from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List, Optional
import os

class Settings(BaseSettings):
    APP_ENV: str = "dev"
    SECRET_KEY: str = "secret"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "postgresql://user:password@localhost/adcopy")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Storage Configuration
    STORAGE_BACKEND: str = os.getenv("STORAGE_BACKEND", "local")
    LOCAL_STORAGE_DIR: str = os.getenv("LOCAL_STORAGE_DIR", "./_data")
    S3_ENDPOINT: str = os.getenv("S3_ENDPOINT", "http://localhost:9000")
    S3_ACCESS_KEY: str = os.getenv("S3_ACCESS_KEY", "minioadmin")
    S3_SECRET_KEY: str = os.getenv("S3_SECRET_KEY", "minioadmin")
    S3_BUCKET: str = os.getenv("S3_BUCKET", "ad-assets")
    
    # Queue Configuration
    QUEUE_MODE: str = os.getenv("QUEUE_MODE", "inline")
    
    # LLM Configuration
    LLM_PROVIDER: str = "groq"
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.1-70b-versatile"
    LOCAL_LLM_ENDPOINT: Optional[str] = None
    LOCAL_LLM_MODEL: str = "llama-3.1-8b-instruct"
    LLM_TIMEOUT_S: int = 30
    LLM_MAX_RETRIES: int = 3
    
    # Production Settings
    CORS_ORIGINS: str = "http://localhost:5173"
    RATE_LIMIT_PER_MINUTE: int = 60
    LOG_LEVEL: str = "INFO"
    SENTRY_DSN: Optional[str] = None
    
    # Brand Voice & Similarity
    BRAND_VOICE_ENABLED: bool = True
    BRAND_VOICE_THRESHOLD: float = 0.7
    DIVERSITY_THRESHOLD: float = 0.8
    
    # Context / RAG
    CONTEXT_DATA_DIR: str = "server/app/data/context"
    CHROMA_PERSIST_DIR: str = "server/app/.chroma"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"  # or all-mpnet-base-v2
    CONTEXT_TOPK_REVIEWS: int = 4
    CONTEXT_TOPK_FEATURES: int = 3
    CONTEXT_TOPK_README: int = 2
    CONTEXT_PRELOAD_ON_STARTUP: bool = True
    
    # Policy & Validation
    POLICY_STRICT_MODE: bool = False
    LOCALE_RULES: str = "en-IN,hi-IN"
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields in .env file

settings = Settings()
