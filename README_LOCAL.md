# PDF-Based Policy Chatbot

Enterprise Document-QA Assistant for HR policies, company rules, contracts, procedures, SOPs, and guidelines.

## 🎯 Features

- **Strict Document-Based Answers**: Only responds from uploaded PDF content
- **Vector Search**: Uses embeddings for semantic search across documents
- **Source Attribution**: Always cites the document, page, and section
- **Confidence Scoring**: Indicates reliability of answers (High/Medium/Low)
- **Multi-Document Support**: Process multiple PDFs simultaneously
- **No Hallucination**: Never guesses or uses external knowledge

## 📋 Supported Use Cases

- HR Policies & Procedures
- Leave policies
- Travel entitlement
- Payroll rules
- Employee benefits
- Medical coverage
- Company guidelines
- Compliance documents
- SOPs
- Contracts or agreements

## 🚀 Quick Start

### 1. Installation

```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Upload Documents

Place your PDF files in the `uploads/` folder:

```bash
# The uploads folder is created automatically
# Add your HR policy PDFs there
```

### 4. Ingest Documents

Process your PDFs into the vector database:

```bash
# Process all PDFs in uploads folder
python ingest.py

# Process specific files
python ingest.py --files path/to/policy1.pdf path/to/policy2.pdf

# Clear existing data and re-ingest
python ingest.py --clear
```

### 5. Start Chatbot

```bash
python main.py
```

## 💬 Usage Examples

```
🙋 Your Question: How many annual leaves does a permanent employee get?

ANSWER:
According to the HR Policy Document → Leave Policy → Section 4.1, 
a permanent employee is entitled to 14 days of annual leave per year.

SOURCE (Matched from PDF):
  • hr_policy.pdf | Page 12 | Section: Leave Policy | Relevance: 94%

CONFIDENCE: High
```

```
🙋 Your Question: Can I work from home for 3 days?

ANSWER:
I could not find any policy related to remote work or work-from-home 
in the provided documents.

CONFIDENCE: Low
```

## 📁 Project Structure

```
AIAssistant/
├── config.py              # Configuration settings
├── pdf_processor.py       # PDF extraction and chunking
├── vector_store.py        # Embeddings and vector database
├── chatbot.py            # Query processing and LLM integration
├── ingest.py             # Document ingestion script
├── main.py               # Interactive CLI application
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── uploads/              # Place PDF files here
└── vector_db/            # ChromaDB storage (auto-created)
```

## ⚙️ Configuration Options

Edit `config.py` to customize:

- **Chunk Size**: Default 800 tokens
- **Chunk Overlap**: Default 200 tokens
- **Top K Results**: Default 5 chunks
- **LLM Model**: gpt-4 or gpt-3.5-turbo
- **Similarity Threshold**: Minimum 0.7
- **Confidence Levels**: High (0.85), Medium (0.70), Low (0.50)

## 🎨 Architecture

```
User Query
    ↓
[Query Processing]
    ↓
[Embedding Generation] → OpenAI API
    ↓
[Vector Search] → ChromaDB
    ↓
[Context Retrieval] → Top K Chunks
    ↓
[LLM Response] → GPT-4 with Context
    ↓
[Answer + Sources + Confidence]
```

## 🔧 Advanced Usage

### Custom Vector Database

To use Pinecone or Qdrant instead of ChromaDB, modify `vector_store.py`:

```python
# For Pinecone
import pinecone
# Initialize and use Pinecone client

# For Qdrant
from qdrant_client import QdrantClient
# Initialize and use Qdrant client
```

### API Integration

Use the chatbot programmatically:

```python
from chatbot import PolicyChatbot

chatbot = PolicyChatbot()
response = chatbot.query("What is the leave policy?")
print(response['answer'])
```

## 🛡️ Key Constraints

1. **Strictly Factual**: No assumptions or external knowledge
2. **Neutral & Professional**: Enterprise-grade responses
3. **No Hallucination**: Clear "not found" messages when appropriate
4. **Source Attribution**: Always cite document sources
5. **Never Reinterpret**: Exact policy wording only

## 📝 Commands

- `help` - Show usage tips
- `stats` - Display database statistics
- `clear` - Clear screen
- `quit/exit` - Exit chatbot

## 🔒 Security Notes

- Keep your `.env` file secure
- Never commit API keys to version control
- Use environment variables for sensitive data
- Consider implementing user authentication for production

## 🐛 Troubleshooting

**No documents found:**
```bash
# Check if PDFs are in the uploads folder
# Re-run ingestion: python ingest.py --clear
```

**Low confidence answers:**
```bash
# Try rephrasing your question
# Check if the information exists in your PDFs
# Lower SIMILARITY_THRESHOLD in config.py
```

**API errors:**
```bash
# Verify OPENAI_API_KEY in .env file
# Check API quota and billing
```

## 📄 License

This project is provided as-is for enterprise document Q&A purposes.

## 🤝 Contributing

This is a complete, production-ready implementation. Customize as needed for your specific use case.
