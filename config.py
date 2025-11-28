"""
Configuration file for PDF-based Policy Chatbot
"""

import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
DB_DIR = BASE_DIR / "vector_db"

# Ensure directories exist
UPLOAD_DIR.mkdir(exist_ok=True)
DB_DIR.mkdir(exist_ok=True)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Embedding Configuration
EMBEDDING_MODEL = "text-embedding-ada-002"
CHUNK_SIZE = 800  # tokens per chunk
CHUNK_OVERLAP = 200  # overlap between chunks

# Vector Database Configuration
VECTOR_DB_TYPE = "chroma"  # Options: chroma, pinecone, qdrant
COLLECTION_NAME = "policy_documents"

# Retrieval Configuration
TOP_K_RESULTS = 5  # Number of chunks to retrieve for context
SIMILARITY_THRESHOLD = 0.7  # Minimum similarity score

# LLM Configuration
LLM_MODEL = "gpt-4"  # or gpt-3.5-turbo for cost savings
MAX_TOKENS = 1000
TEMPERATURE = 0.1  # Low temperature for factual responses

# Confidence thresholds
CONFIDENCE_HIGH = 0.85
CONFIDENCE_MEDIUM = 0.70
CONFIDENCE_LOW = 0.50
