"""
Configuration file for PDF-based Policy Chatbot
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Project paths
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
DB_DIR = BASE_DIR / "vector_db"

# Ensure directories exist
UPLOAD_DIR.mkdir(exist_ok=True)
DB_DIR.mkdir(exist_ok=True)

# DeepSeek API Configuration
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Fallback to OpenAI if DeepSeek key not provided
# Fallback to OpenAI if DeepSeek key not provided
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Embedding Configuration
# Note: DeepSeek doesn't have a native embedding model, so we'll use sentence-transformers locally
EMBEDDING_MODEL = "text-embedding-3-small"  # For OpenAI
LOCAL_EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # For local embeddings
USE_LOCAL_EMBEDDINGS = True  # Set to True to use local embeddings instead of API
CHUNK_SIZE = 500  # tokens per chunk
CHUNK_OVERLAP = 100  # overlap between chunks

# Vector Database Configuration
VECTOR_DB_TYPE = "chroma"  # Options: chroma, pinecone, qdrant
COLLECTION_NAME = "policy_documents"

# Retrieval Configuration
TOP_K_RESULTS = 30  # Number of chunks to retrieve for context
SIMILARITY_THRESHOLD = 0.45  # Minimum similarity score (Increased from 0.3)

# LLM Configuration
LLM_MODEL = "gpt-4o"  # OpenAI model
MAX_TOKENS = 1000
TEMPERATURE = 0.1  # Low temperature for factual responses

# Confidence thresholds
CONFIDENCE_HIGH = 0.60  # Increased from 0.55
CONFIDENCE_MEDIUM = 0.50  # Increased from 0.35
CONFIDENCE_LOW = 0.40  # Increased from 0.25

# LLM Provider Configuration
# Options: "openai", "deepseek", "gemini"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

if LLM_PROVIDER == "deepseek":
    LLM_MODEL = "deepseek-chat"
    API_KEY = DEEPSEEK_API_KEY
    BASE_URL = DEEPSEEK_BASE_URL
elif LLM_PROVIDER == "gemini":
    LLM_MODEL = "gemini-pro"
    API_KEY = GEMINI_API_KEY
    BASE_URL = None
else:
    LLM_MODEL = "gpt-4o"
    API_KEY = OPENAI_API_KEY
    BASE_URL = None
