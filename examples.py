"""
Example Usage Script
Demonstrates how to use the Policy Chatbot programmatically
"""

from dotenv import load_dotenv
from chatbot import PolicyChatbot
from vector_store import VectorStore
from pdf_processor import PDFProcessor

# Load environment variables
load_dotenv()


def example_basic_usage():
    """Basic chatbot usage example"""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 60)
    
    # Initialize chatbot
    chatbot = PolicyChatbot()
    
    # Ask a question
    question = "How many annual leaves does a permanent employee get?"
    print(f"\nQuestion: {question}")
    
    # Get response
    response = chatbot.query(question)
    
    # Display formatted response
    print("\n" + chatbot.format_response(response))


def example_batch_queries():
    """Process multiple queries"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Batch Queries")
    print("=" * 60)
    
    chatbot = PolicyChatbot()
    
    questions = [
        "What is the notice period for resignation?",
        "Can I work from home?",
        "What are the medical benefits?",
        "What is the travel reimbursement policy?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n\n--- Query {i} ---")
        print(f"Q: {question}")
        
        response = chatbot.query(question)
        print(f"\nA: {response['answer']}")
        print(f"Confidence: {response['confidence']}")


def example_programmatic_access():
    """Access response components programmatically"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Programmatic Access")
    print("=" * 60)
    
    chatbot = PolicyChatbot()
    
    question = "What is the maternity leave policy?"
    response = chatbot.query(question)
    
    # Access individual components
    print(f"\nQuestion: {question}")
    print(f"\nAnswer: {response['answer']}")
    print(f"\nConfidence: {response['confidence']}")
    print(f"\nContext Chunks Used: {response['context_chunks']}")
    
    print("\nSources:")
    for source in response['sources']:
        print(f"  - {source['document']} (Page {source['page']})")


def example_vector_search():
    """Direct vector search example"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Direct Vector Search")
    print("=" * 60)
    
    vector_store = VectorStore()
    
    query = "sick leave"
    results = vector_store.search(query, top_k=3)
    
    print(f"\nQuery: {query}")
    print(f"Results found: {results['total_results']}")
    
    for i, result in enumerate(results['results'], 1):
        print(f"\n--- Result {i} ---")
        print(f"Text: {result['text'][:200]}...")
        print(f"Source: {result['metadata']['filename']}")
        print(f"Page: {result['metadata']['page_number']}")
        print(f"Similarity: {result['similarity_score']:.2%}")


def example_pdf_processing():
    """PDF processing example"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: PDF Processing")
    print("=" * 60)
    
    # Note: This requires an actual PDF file
    # Uncomment and modify the path to use
    
    # processor = PDFProcessor()
    # pdf_path = "uploads/sample_policy.pdf"
    # chunks = processor.process_pdf(pdf_path)
    # 
    # print(f"\nProcessed: {pdf_path}")
    # print(f"Total chunks: {len(chunks)}")
    # print(f"\nFirst chunk preview:")
    # print(chunks[0]['text'][:200])
    
    print("\nSkipped - no PDF file specified")


def example_database_stats():
    """Database statistics example"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Database Statistics")
    print("=" * 60)
    
    vector_store = VectorStore()
    stats = vector_store.get_collection_stats()
    
    print(f"\nCollection Name: {stats['collection_name']}")
    print(f"Total Chunks: {stats['total_chunks']}")
    
    if stats['total_chunks'] > 0:
        print("\n✅ Database is ready for queries")
    else:
        print("\n⚠️  Database is empty. Run 'python ingest.py' first")


def example_custom_response_format():
    """Custom response formatting example"""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Custom Response Formatting")
    print("=" * 60)
    
    chatbot = PolicyChatbot()
    
    question = "What is the probation period?"
    response = chatbot.query(question)
    
    # Custom JSON format
    import json
    custom_response = {
        "question": question,
        "answer": response['answer'],
        "confidence": response['confidence'],
        "sources": [
            {
                "document": s['document'],
                "page": s['page'],
                "relevance": f"{s['similarity']:.0%}"
            }
            for s in response['sources']
        ]
    }
    
    print("\nCustom JSON Response:")
    print(json.dumps(custom_response, indent=2))


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print(" PDF POLICY CHATBOT - USAGE EXAMPLES ".center(70))
    print("=" * 70)
    
    try:
        example_database_stats()
        example_basic_usage()
        example_batch_queries()
        example_programmatic_access()
        example_vector_search()
        example_pdf_processing()
        example_custom_response_format()
        
        print("\n" + "=" * 70)
        print("All examples completed!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        print("\nMake sure you have:")
        print("1. Set up your .env file with OPENAI_API_KEY")
        print("2. Run 'python ingest.py' to load documents")


if __name__ == "__main__":
    main()
