---
title: AI Policy Assistant
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# AI Policy Assistant

Enterprise Document-QA Assistant for HR policies, company rules, contracts, procedures, SOPs, and guidelines.

## Features

- **Strict Document-Based Answers**: Only responds from uploaded PDF content
- **Vector Search**: Uses embeddings for semantic search across documents
- **Source Attribution**: Always cites the document, page, and section
- **Confidence Scoring**: Indicates reliability of answers (High/Medium/Low)
- **Multi-Document Support**: Process multiple PDFs simultaneously

## Setup

### Environment Variables

You need to set the following secret in Hugging Face Spaces:

- `OPENAI_API_KEY`: Your OpenAI API key for embeddings and LLM

### Usage

1. Upload PDF documents using the upload interface
2. Wait for ingestion to complete
3. Ask questions about your policies
4. Get answers with source citations and confidence scores

## Architecture

- **Backend**: FastAPI + Python
- **Frontend**: React + Vite + Tailwind CSS
- **Vector Store**: ChromaDB
- **LLM**: OpenAI GPT-4 / GPT-3.5
- **Embeddings**: OpenAI text-embedding-ada-002

## API Endpoints

- `POST /query` - Ask questions
- `POST /upload` - Upload PDF documents
- `GET /stats` - Get collection statistics
- `POST /reingest` - Re-process all documents

## Local Development

```bash
# Backend
pip install -r requirements.txt
python api.py

# Frontend
cd frontend
npm install
npm run dev
```

## License

MIT License
