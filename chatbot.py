"""
Policy Chatbot Module
Handles query processing and response generation
"""

from typing import Dict, List
from openai import OpenAI
import os

from config import (
    OPENAI_API_KEY,
    LLM_MODEL,
    MAX_TOKENS,
    TEMPERATURE,
    SIMILARITY_THRESHOLD,
    CONFIDENCE_HIGH,
    CONFIDENCE_MEDIUM,
    CONFIDENCE_LOW,
    LLM_PROVIDER,
    API_KEY,
    BASE_URL,
)
from vector_store import VectorStore


class PolicyChatbot:
    """Enterprise Document-QA Assistant for HR Policies"""
    
    def __init__(self):
        self.provider = LLM_PROVIDER
        self.api_key = API_KEY
        
        if not self.api_key:
            raise ValueError(f"API Key for {self.provider} is not set in environment variables.")
            
        if self.provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.model =  genai.GenerativeModel(LLM_MODEL)
        else:
            # OpenAI or DeepSeek
            from openai import OpenAI
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=BASE_URL
            )
            self.model = LLM_MODEL
            
        self.vector_store = VectorStore()
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """Create the master system prompt"""
        return """You are an enterprise Document-QA Assistant. Your job is to answer user questions based on the information extracted from the uploaded PDF documents.

**GUIDELINES:**

1. **Primary Source**: Use the provided CONTEXT to answer the question.
2. **Partial Answers**: If the context contains information that *partially* answers the question, provide that information and mention what is missing. Do not simply refuse to answer.
3. **No Hallucination**: Do not make up facts. If the information is completely missing, state that clearly.
4. **Professional Tone**: Be helpful, factual, and professional.
5. **Citations**: Always mention the source document and section when possible.
6. **Formatting**: Use **Markdown** to format your response.
   - Use **bullet points** for lists.
   - Use **bold** for key terms.
   - Use headings where appropriate.

**When answering:**
- Start with the direct answer if available.
- Quote relevant policy clauses.
- If the user asks about a general topic (e.g., "leave"), summarize the available leave policies found in the context.
- If the exact answer isn't found but related info is, say: "I couldn't find the exact answer, but here is what the policy says about [related topic]..."

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
    
    def _enhance_query(self, query: str) -> str:
        """Enhance user query for better semantic search"""
        query_lower = query.lower()
        
        # Expand common short queries with more context
        if 'leave' in query_lower and 'policy' in query_lower:
            return f"{query} leave entitlement annual leave sick leave vacation policy employee leave rules time off"
        elif 'leave' in query_lower:
            return f"{query} leave policy leave entitlement annual leave sick leave"
        elif 'travel' in query_lower:
            return f"{query} travel policy travel allowance business travel expense"
        elif 'salary' in query_lower or 'payroll' in query_lower:
            return f"{query} salary payroll compensation pay structure"
        elif 'medical' in query_lower or 'health' in query_lower:
            return f"{query} medical insurance health coverage healthcare benefits"
        
        return query
    
    def query(self, user_question: str) -> Dict[str, any]:
        """
        Process user query and generate response
        
        Args:
            user_question: User's question
            
        Returns:
            Response dictionary with answer, source, and confidence
        """
        # Step 1: Enhance the query for better semantic matching
        enhanced_query = self._enhance_query(user_question)
        
        # Step 2: Retrieve relevant context
        search_results = self.vector_store.search(enhanced_query)
        
        # Debug: Print similarity scores
        print(f"\n🔍 Search Results for: '{user_question}'")
        print(f"Enhanced query: '{enhanced_query}'")
        print(f"Total results: {len(search_results['results'])}")
        if search_results['results']:
            print("Top 5 similarity scores:")
            for i, r in enumerate(search_results['results'][:5], 1):
                print(f"  {i}. Score: {r['similarity_score']:.3f} | {r['metadata'].get('filename', 'Unknown')}")
        print()
        
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
        # Debug: Print context to terminal to see what the LLM is reading
        print("\n" + "="*50)
        print(f"DEBUG: Context sent to LLM for question: '{question}'")
        print("-" * 20)
        print(context[:1000] + "..." if len(context) > 1000 else context)
        print("="*50 + "\n")

        user_prompt = f"""CONTEXT (from PDF documents):
{context}

---

USER QUESTION:
{question}

---

INSTRUCTIONS:
1. Read the USER QUESTION carefully and understand what specific information is being asked
2. Search through the CONTEXT above for information that DIRECTLY answers this question
3. Answer ONLY the specific question asked - do not provide general background information unless it directly answers the question
4. If the CONTEXT contains information about the topic asked (e.g., leave policy), provide ONLY that specific policy information
5. Do NOT provide general organizational information or scope sections unless that's what was asked
6. Cite the specific document, section, and page number for your answer
7. If the specific answer is not in the context, say: "I could not find this information in the provided documents."
8. Be clear, concise, and directly answer the question"""

        try:
            if self.provider == "gemini":
                # Prepare prompt for Gemini
                gemini_prompt = f"{self.system_prompt}\n\n{user_prompt}"
                response = self.model.generate_content(gemini_prompt)
                return response.text.strip()
            else:
                # OpenAI / DeepSeek
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE,
                )
                return response.choices[0].message.content.strip()
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"Error generating response: {str(e)}"
    
    def _calculate_confidence(self, chunks: List[Dict[str, any]]) -> str:
        """Calculate confidence level based on similarity scores"""
        if not chunks:
            return "Low"
        
        # Use the MAXIMUM similarity score instead of average
        # If we found at least one very good match, we are confident.
        max_similarity = max(c['similarity_score'] for c in chunks)
        
        if max_similarity >= CONFIDENCE_HIGH:
            return "High"
        elif max_similarity >= CONFIDENCE_MEDIUM:
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
