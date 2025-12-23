
from chatbot import PolicyChatbot
import sys

def test_chatbot():
    print("Initializing Chatbot...")
    try:
        bot = PolicyChatbot()
        print("Chatbot initialized.")
        
        query = "want to know about Leave Policy?"
        print(f"Running query: {query}")
        
        response = bot.query(query)
        
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(f"Response:\n{response['answer']}\n\n")
            if response['sources']:
                f.write("Sources:\n")
                for source in response['sources']:
                    f.write(f"- {source['document']} ({source['similarity']})\n")
        
        print("Done. Check result.txt")
                
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chatbot()
