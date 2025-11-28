# System Architecture - PDF Policy Chatbot

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                   (CLI / API / Web Interface)                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CHATBOT LAYER                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Policy Chatbot (chatbot.py)                             │  │
│  │  - Query Processing                                      │  │
│  │  - Context Preparation                                   │  │
│  │  - Response Generation                                   │  │
│  │  - Confidence Calculation                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   VECTOR STORE LAYER     │  │      LLM LAYER           │
│  (vector_store.py)       │  │   (OpenAI API)           │
│                          │  │                          │
│  - Embedding Generation  │  │  - GPT-4 / GPT-3.5       │
│  - Similarity Search     │  │  - Response Generation   │
│  - ChromaDB Management   │  │  - Context Understanding │
└────────┬─────────────────┘  └──────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   VECTOR DATABASE                               │
│                      (ChromaDB)                                 │
│  - Document Embeddings Storage                                  │
│  - Semantic Search                                              │
│  - Metadata Management                                          │
└────────────────────────────┬────────────────────────────────────┘
                             ▲
                             │
┌─────────────────────────────────────────────────────────────────┐
│                   INGESTION LAYER                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  PDF Processor (pdf_processor.py)                        │  │
│  │  - Text Extraction                                       │  │
│  │  - Chunking with Overlap                                 │  │
│  │  - Metadata Extraction                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             ▲
                             │
┌─────────────────────────────────────────────────────────────────┐
│                      DATA SOURCE                                │
│                   PDF Documents (uploads/)                      │
│  - HR Policies                                                  │
│  - Company Guidelines                                           │
│  - SOPs & Procedures                                            │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### 1. Document Ingestion Pipeline

```
PDF Upload → Text Extraction → Chunking → Embedding → Vector Store
```

**Detailed Steps:**

1. **PDF Upload**: User places PDF in `uploads/` folder
2. **Text Extraction** (pdf_processor.py):
   - PyPDF2 extracts text page by page
   - Section headings are identified
   - Metadata is collected (filename, page numbers)
3. **Chunking**:
   - Text split into 800-token chunks
   - 200-token overlap between chunks
   - Preserves context across chunk boundaries
4. **Embedding Generation**:
   - OpenAI text-embedding-ada-002
   - Converts text to 1536-dimensional vectors
5. **Vector Store**:
   - ChromaDB stores embeddings + metadata
   - Enables semantic similarity search

### 2. Query Processing Pipeline

```
User Query → Embedding → Similarity Search → Context Retrieval 
    → LLM Processing → Response + Sources + Confidence
```

**Detailed Steps:**

1. **User Query**: Question entered via CLI/API
2. **Query Embedding**:
   - Query converted to vector using same model
3. **Similarity Search**:
   - ChromaDB finds top K most similar chunks
   - Cosine similarity ranking
4. **Context Filtering**:
   - Chunks filtered by similarity threshold (0.7)
   - Top 5 relevant chunks selected
5. **LLM Processing**:
   - GPT-4 receives system prompt + context + query
   - Temperature: 0.1 (factual, deterministic)
   - Max tokens: 1000
6. **Response Generation**:
   - Answer extracted from context only
   - Source attribution added
   - Confidence calculated from similarity scores

## 🏗️ Component Architecture

### Core Modules

#### 1. **config.py**
- Central configuration
- Environment variables
- Hyperparameters
- Path management

#### 2. **pdf_processor.py**
```
PDFProcessor
├── extract_text_from_pdf()
├── chunk_text()
├── _extract_section_heading()
└── _clean_text()
```

#### 3. **vector_store.py**
```
VectorStore
├── generate_embedding()
├── add_documents()
├── search()
├── clear_database()
└── get_collection_stats()
```

#### 4. **chatbot.py**
```
PolicyChatbot
├── query()
├── _prepare_context()
├── _generate_response()
├── _calculate_confidence()
├── _extract_sources()
└── format_response()
```

#### 5. **ingest.py**
- CLI for document ingestion
- Batch processing
- Progress tracking

#### 6. **main.py**
- Interactive chatbot interface
- Command handling
- User interaction

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                          │
├─────────────────────────────────────────────────────────────┤
│  1. Environment Variables (.env)                            │
│     - API keys isolated from code                           │
│     - Never committed to version control                    │
├─────────────────────────────────────────────────────────────┤
│  2. Input Validation                                        │
│     - File type checking                                    │
│     - Path sanitization                                     │
├─────────────────────────────────────────────────────────────┤
│  3. Output Sanitization                                     │
│     - LLM output validation                                 │
│     - Source attribution verification                       │
├─────────────────────────────────────────────────────────────┤
│  4. Access Control                                          │
│     - Local file system only                                │
│     - No external network access (except OpenAI API)        │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Data Model

### Document Chunk Structure
```json
{
  "chunk_id": 42,
  "text": "Employees are entitled to...",
  "metadata": {
    "filename": "hr_policy.pdf",
    "page_number": 15,
    "section": "Leave Policy",
    "chunk_index": 42,
    "token_count": 750
  }
}
```

### Search Result Structure
```json
{
  "query": "annual leave policy",
  "results": [
    {
      "text": "Chunk text...",
      "metadata": {...},
      "similarity_score": 0.89
    }
  ],
  "total_results": 5
}
```

### Response Structure
```json
{
  "answer": "According to...",
  "sources": [
    {
      "document": "hr_policy.pdf",
      "page": 15,
      "section": "Leave Policy",
      "similarity": 0.89
    }
  ],
  "confidence": "High",
  "context_chunks": 5
}
```

## ⚡ Performance Optimization

### 1. Chunking Strategy
- **Size**: 800 tokens (optimal for context/granularity)
- **Overlap**: 200 tokens (preserves context)
- **Trade-off**: Memory vs. Accuracy

### 2. Embedding Caching
- Cache frequently used embeddings
- Reduce API calls
- Faster response time

### 3. Batch Processing
- Process multiple documents together
- Parallel embedding generation possible
- Progress tracking

### 4. Vector Database Optimization
- ChromaDB persistent storage
- Fast similarity search (ANN)
- Metadata indexing

## 🔧 Configuration Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| CHUNK_SIZE | 800 | Tokens per chunk |
| CHUNK_OVERLAP | 200 | Overlap between chunks |
| TOP_K_RESULTS | 5 | Chunks retrieved |
| SIMILARITY_THRESHOLD | 0.7 | Minimum relevance |
| LLM_MODEL | gpt-4 | Language model |
| TEMPERATURE | 0.1 | Response randomness |
| CONFIDENCE_HIGH | 0.85 | High confidence threshold |
| CONFIDENCE_MEDIUM | 0.70 | Medium confidence threshold |

## 🚀 Scalability Considerations

### Current Design (Single User)
- Local ChromaDB
- Synchronous processing
- CLI interface

### Production Scalability
- **Multi-User**: Add authentication layer
- **Distributed Vector DB**: Pinecone, Qdrant Cloud
- **API Server**: FastAPI/Flask wrapper
- **Caching**: Redis for embeddings
- **Load Balancing**: Multiple LLM endpoints
- **Monitoring**: Logging, metrics, alerts

## 🔍 Error Handling

```
User Input → Validation → Processing → Error Handling → Response
                ↓             ↓             ↓
            InvalidInput  NoContext    APIError
                ↓             ↓             ↓
            UserMessage   LowConfidence  Retry/Fallback
```

## 📈 Metrics & Monitoring

### Key Metrics
- **Ingestion**: Documents processed, chunks created
- **Search**: Average similarity score, retrieval time
- **Response**: Confidence distribution, source coverage
- **API**: OpenAI token usage, costs

### Logging Points
- Document ingestion start/complete
- Embedding generation (batches)
- Search queries and results
- LLM API calls
- Errors and exceptions

## 🎯 Design Principles

1. **Single Source of Truth**: Only PDF documents
2. **Transparency**: Always show sources
3. **Accuracy over Creativity**: Low temperature, strict prompts
4. **Fail-Safe**: Clear "not found" messages
5. **Modularity**: Swappable components (LLM, Vector DB)
6. **Maintainability**: Clear separation of concerns
