"""
Policy Chatbot Module
Handles query processing and response generation
"""

from typing import Dict, List
from openai import OpenAI

from config import (
    OPENAI_API_KEY,
    LLM_MODEL,
    MAX_TOKENS,
    TEMPERATURE,
    SIMILARITY_THRESHOLD,
    CONFIDENCE_HIGH,
    CONFIDENCE_MEDIUM,
    CONFIDENCE_LOW
)
from vector_store import VectorStore


class PolicyChatbot:
    """Enterprise Document-QA Assistant for HR Policies"""
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.vector_store = VectorStore()
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """Create the master system prompt"""
        return """You are an enterprise Document-QA Assistant. Your job is to answer user questions strictly based on the information extracted from the uploaded PDF documents (HR policies, company rules, contracts, procedures, SOPs, guidelines, etc.).

**CRITICAL RULES:**

1. ONLY use information from the provided CONTEXT (extracted from PDF documents)
2. If the answer is NOT in the context, respond: "I could not find this information in the provided documents."
3. NEVER guess or use external knowledge
4. NEVER hallucinate or make assumptions
5. Be strictly factual, neutral, and professional
6. NEVER rewrite or reinterpret policy meanings

**When answering:**
- Provide clear, concise answers in simple language
- Give exact policy rules, clauses, or guidelines
- Mention the source (document name, section, page number)
- If multiple relevant sections exist, summarize all of them

**Supported topics:**
- HR Policies & Procedures
- Leave policies
- Travel entitlement
- Payroll rules
- Employee benefits
- Medical coverage
- Company guidelines
- Compliance documents
- SOPs
- Contracts or agreements"""
    
    def query(self, user_question: str) -> Dict[str, any]:
        """
        Process user query and generate response
        
        Args:
            user_question: User's question
            
        Returns:
            Response dictionary with answer, source, and confidence
        """
        # Step 1: Retrieve relevant context
        search_results = self.vector_store.search(user_question)
        
        # Step 2: Check if we have relevant results
        if not search_results['results']:
            return self._no_context_response()
        
        # Step 3: Filter by similarity threshold
        relevant_chunks = [
            r for r in search_results['results'] 
            if r['similarity_score'] >= SIMILARITY_THRESHOLD
        ]
        
        if not relevant_chunks:
            return self._low_confidence_response()
        
        # Step 4: Prepare context
        context = self._prepare_context(relevant_chunks)
        
        # Step 5: Generate response
        response = self._generate_response(user_question, context)
        
        # Step 6: Determine confidence
        confidence = self._calculate_confidence(relevant_chunks)
        
        # Step 7: Extract sources
        sources = self._extract_sources(relevant_chunks)
        
        return {
            'answer': response,
            'sources': sources,
            'confidence': confidence,
            'context_chunks': len(relevant_chunks)
        }
    
    def _prepare_context(self, chunks: List[Dict[str, any]]) -> str:
        """Prepare context from retrieved chunks"""
        context_parts = []
        
        for i, chunk in enumerate(chunks, 1):
            metadata = chunk['metadata']
            source_info = (
                f"[Source {i}: {metadata.get('filename', 'Unknown')} | "
                f"Page {metadata.get('page_number', 'N/A')} | "
                f"Section: {metadata.get('section', 'General')}]"
            )
            context_parts.append(f"{source_info}\n{chunk['text']}\n")
        
        return "\n---\n".join(context_parts)
    
    def _generate_response(self, question: str, context: str) -> str:
        """Generate response using LLM"""
        user_prompt = f"""CONTEXT (from PDF documents):
{context}

---

USER QUESTION:
{question}

---

Provide your answer following these rules:
- Answer ONLY using the CONTEXT provided above
- If the answer is not in the context, say: "I could not find this information in the provided documents."
- Mention the specific document, section, or page where you found the information
- Be clear, concise, and factual"""

        try:
            response = self.client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _calculate_confidence(self, chunks: List[Dict[str, any]]) -> str:
        """Calculate confidence level based on similarity scores"""
        if not chunks:
            return "Low"
        
        avg_similarity = sum(c['similarity_score'] for c in chunks) / len(chunks)
        
        if avg_similarity >= CONFIDENCE_HIGH:
            return "High"
        elif avg_similarity >= CONFIDENCE_MEDIUM:
            return "Medium"
        else:
            return "Low"
    
    def _extract_sources(self, chunks: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """Extract source information from chunks"""
        sources = []
        seen = set()
        
        for chunk in chunks:
            metadata = chunk['metadata']
            source_key = (
                metadata.get('filename'),
                metadata.get('page_number'),
                metadata.get('section')
            )
            
            if source_key not in seen:
                sources.append({
                    'document': metadata.get('filename', 'Unknown'),
                    'page': metadata.get('page_number', 'N/A'),
                    'section': metadata.get('section', 'General'),
                    'similarity': chunk['similarity_score']
                })
                seen.add(source_key)
        
        return sources
    
    def _no_context_response(self) -> Dict[str, any]:
        """Response when no context is available"""
        return {
            'answer': "I could not find this information in the provided documents.",
            'sources': [],
            'confidence': "Low",
            'context_chunks': 0
        }
    
    def _low_confidence_response(self) -> Dict[str, any]:
        """Response when confidence is too low"""
        return {
            'answer': "Sorry, I cannot retrieve relevant information from the documents. Please upload a more clear or complete version.",
            'sources': [],
            'confidence': "Low",
            'context_chunks': 0
        }
    
    def format_response(self, response: Dict[str, any]) -> str:
        """Format response for display"""
        output = []
        
        output.append("ANSWER:")
        output.append(response['answer'])
        output.append("")
        
        if response['sources']:
            output.append("SOURCE (Matched from PDF):")
            for source in response['sources']:
                output.append(
                    f"  • {source['document']} | "
                    f"Page {source['page']} | "
                    f"Section: {source['section']} | "
                    f"Relevance: {source['similarity']:.2%}"
                )
            output.append("")
        
        output.append(f"CONFIDENCE: {response['confidence']}")
        
        return "\n".join(output)
