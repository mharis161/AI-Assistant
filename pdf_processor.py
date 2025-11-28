"""
PDF Ingestion Module
Handles PDF text extraction and chunking
"""

import re
from typing import List, Dict
from pathlib import Path
import PyPDF2
import tiktoken

from config import CHUNK_SIZE, CHUNK_OVERLAP


class PDFProcessor:
    """Processes PDF files for document ingestion"""
    
    def __init__(self):
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def extract_text_from_pdf(self, pdf_path: str) -> Dict[str, any]:
        """
        Extract text from PDF with metadata
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with text content and metadata
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                text_content = []
                metadata = {
                    'filename': Path(pdf_path).name,
                    'total_pages': len(pdf_reader.pages),
                    'sections': []
                }
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    
                    if page_text.strip():
                        text_content.append({
                            'page_number': page_num,
                            'text': page_text,
                            'section': self._extract_section_heading(page_text)
                        })
                
                return {
                    'content': text_content,
                    'metadata': metadata
                }
                
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
    
    def _extract_section_heading(self, text: str) -> str:
        """Extract section/chapter heading from text"""
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            # Look for common heading patterns
            if re.match(r'^(Chapter|Section|Article|\d+\.)', line, re.IGNORECASE):
                return line[:100]  # Limit heading length
        return "General"
    
    def chunk_text(self, document_data: Dict[str, any]) -> List[Dict[str, any]]:
        """
        Split document into chunks with overlap
        
        Args:
            document_data: Extracted document data
            
        Returns:
            List of text chunks with metadata
        """
        chunks = []
        chunk_id = 0
        
        for page_data in document_data['content']:
            page_text = page_data['text']
            page_num = page_data['page_number']
            section = page_data['section']
            
            # Tokenize the text
            tokens = self.encoding.encode(page_text)
            
            # Create overlapping chunks
            start = 0
            while start < len(tokens):
                end = min(start + CHUNK_SIZE, len(tokens))
                chunk_tokens = tokens[start:end]
                chunk_text = self.encoding.decode(chunk_tokens)
                
                # Clean up the chunk
                chunk_text = self._clean_text(chunk_text)
                
                if chunk_text.strip():
                    chunks.append({
                        'chunk_id': chunk_id,
                        'text': chunk_text,
                        'metadata': {
                            'filename': document_data['metadata']['filename'],
                            'page_number': page_num,
                            'section': section,
                            'chunk_index': chunk_id,
                            'token_count': len(chunk_tokens)
                        }
                    })
                    chunk_id += 1
                
                # Move to next chunk with overlap
                start = end - CHUNK_OVERLAP if end < len(tokens) else end
                
                if start >= len(tokens):
                    break
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\-\(\)\[\]\/\&\%\$\#\@\!\?]', '', text)
        return text.strip()
    
    def process_pdf(self, pdf_path: str) -> List[Dict[str, any]]:
        """
        Complete PDF processing pipeline
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of processed chunks
        """
        print(f"Processing PDF: {pdf_path}")
        
        # Extract text
        document_data = self.extract_text_from_pdf(pdf_path)
        print(f"Extracted {document_data['metadata']['total_pages']} pages")
        
        # Create chunks
        chunks = self.chunk_text(document_data)
        print(f"Created {len(chunks)} chunks")
        
        return chunks


def process_multiple_pdfs(pdf_paths: List[str]) -> List[Dict[str, any]]:
    """
    Process multiple PDF files
    
    Args:
        pdf_paths: List of PDF file paths
        
    Returns:
        Combined list of chunks from all PDFs
    """
    processor = PDFProcessor()
    all_chunks = []
    
    for pdf_path in pdf_paths:
        try:
            chunks = processor.process_pdf(pdf_path)
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"Error processing {pdf_path}: {str(e)}")
            continue
    
    return all_chunks
