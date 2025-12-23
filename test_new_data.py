
from chatbot import PolicyChatbot
import sys

def test_new_data():
    print("Initializing Chatbot...")
    try:
        bot = PolicyChatbot()
        print("Chatbot initialized.")
        
        # Ask a relevant question for the NEW data
        query = "What are the rules for Murabaha transaction?"
        print(f"\nRunning relevant query: {query}")
        print("-" * 50)
        
        response = bot.query(query)
        
        print("\nResponse:")
        print(response['answer'])
        
        if response['sources']:
            print("\nSources found:")
            for source in response['sources']:
                print(f"- {source['document']} (Score: {source['similarity']:.3f})")
                
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_new_data()
