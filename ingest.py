"""
Document Ingestion Script
Use this script to upload and process PDF documents
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from pdf_processor import process_multiple_pdfs
from vector_store import VectorStore
from config import UPLOAD_DIR

# Load environment variables
load_dotenv()


def ingest_documents(pdf_paths: list = None, clear_existing: bool = False):
    """
    Ingest PDF documents into the vector store
    
    Args:
        pdf_paths: List of PDF file paths. If None, process all PDFs in uploads folder
        clear_existing: Whether to clear existing data before ingestion
    """
    print("=" * 60)
    print("PDF DOCUMENT INGESTION SYSTEM")
    print("=" * 60)
    
    # Initialize vector store
    vector_store = VectorStore()
    
    # Clear existing data if requested
    if clear_existing:
        print("\n⚠️  Clearing existing vector store...")
        vector_store.clear_database()
    
    # Get PDF paths
    if pdf_paths is None:
        pdf_paths = list(UPLOAD_DIR.glob("*.pdf"))
        if not pdf_paths:
            print(f"\n❌ No PDF files found in {UPLOAD_DIR}")
            print(f"Please add PDF files to the uploads folder.")
            return
    
    print(f"\n📄 Found {len(pdf_paths)} PDF file(s) to process:")
    for path in pdf_paths:
        print(f"  • {Path(path).name}")
    
    # Process PDFs
    print("\n🔄 Processing PDFs...")
    chunks = process_multiple_pdfs([str(p) for p in pdf_paths])
    
    if not chunks:
        print("\n❌ No content extracted from PDFs")
        return
    
    print(f"\n✅ Total chunks created: {len(chunks)}")
    
    # Add to vector store
    print("\n🔄 Generating embeddings and storing in vector database...")
    vector_store.add_documents(chunks)
    
    # Show stats
    stats = vector_store.get_collection_stats()
    print("\n" + "=" * 60)
    print("✅ INGESTION COMPLETE!")
    print("=" * 60)
    print(f"Total chunks in database: {stats['total_chunks']}")
    print(f"Collection name: {stats['collection_name']}")
    print("\n💡 You can now start querying the chatbot!")


def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Ingest PDF documents into the Policy Chatbot"
    )
    parser.add_argument(
        '--files',
        nargs='+',
        help='Specific PDF files to ingest'
    )
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear existing database before ingestion'
    )
    
    args = parser.parse_args()
    
    try:
        ingest_documents(
            pdf_paths=args.files,
            clear_existing=args.clear
        )
    except Exception as e:
        print(f"\n❌ Error during ingestion: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
