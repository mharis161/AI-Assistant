"""
Main Application - PDF Policy Chatbot
Interactive chatbot for querying HR policies and documents
"""

import sys
from dotenv import load_dotenv

from chatbot import PolicyChatbot
from vector_store import VectorStore

# Load environment variables
load_dotenv()


class ChatbotCLI:
    """Command-line interface for the chatbot"""
    
    def __init__(self):
        self.chatbot = PolicyChatbot()
        self.vector_store = VectorStore()
    
    def print_banner(self):
        """Print welcome banner"""
        print("\n" + "=" * 70)
        print(" 📋 POLICY CHATBOT - HR Document Assistant ".center(70))
        print("=" * 70)
        
        # Show database stats
        stats = self.vector_store.get_collection_stats()
        print(f"\n📊 Database Status: {stats['total_chunks']} chunks loaded")
        
        if stats['total_chunks'] == 0:
            print("\n⚠️  WARNING: No documents in database!")
            print("Please run: python ingest.py")
            print("Add your PDF files to the 'uploads' folder first.\n")
            return False
        
        print("\n💡 Ask me questions about your company policies!")
        print("Type 'quit' or 'exit' to end the session")
        print("Type 'help' for usage tips\n")
        return True
    
    def print_help(self):
        """Print help message"""
        print("\n" + "=" * 70)
        print("HELP - How to Use the Policy Chatbot")
        print("=" * 70)
        print("""
✅ Example Questions:
  • How many annual leaves does a permanent employee get?
  • What is the notice period for resignation?
  • Can I work from home?
  • What are the medical benefits?
  • What is the travel reimbursement policy?
  • How do I apply for maternity leave?

✅ Tips:
  • Be specific in your questions
  • The chatbot only answers from uploaded PDF documents
  • If information is not found, try rephrasing your question
  • Check the SOURCE section to verify the information

✅ Commands:
  • help  - Show this help message
  • quit  - Exit the chatbot
  • clear - Clear the screen
  • stats - Show database statistics
""")
    
    def print_stats(self):
        """Print database statistics"""
        stats = self.vector_store.get_collection_stats()
        print(f"\n📊 Database Statistics:")
        print(f"  • Total chunks: {stats['total_chunks']}")
        print(f"  • Collection: {stats['collection_name']}")
    
    def run(self):
        """Run the interactive chatbot"""
        # Show banner
        if not self.print_banner():
            sys.exit(1)
        
        # Main loop
        while True:
            try:
                # Get user input
                user_input = input("\n🙋 Your Question: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thank you for using Policy Chatbot. Goodbye!\n")
                    break
                
                if user_input.lower() == 'help':
                    self.print_help()
                    continue
                
                if user_input.lower() == 'clear':
                    print("\n" * 50)
                    self.print_banner()
                    continue
                
                if user_input.lower() == 'stats':
                    self.print_stats()
                    continue
                
                # Process query
                print("\n🤔 Searching documents...")
                response = self.chatbot.query(user_input)
                
                # Format and display response
                print("\n" + "-" * 70)
                formatted_response = self.chatbot.format_response(response)
                print(formatted_response)
                print("-" * 70)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                continue


def main():
    """Main entry point"""
    try:
        cli = ChatbotCLI()
        cli.run()
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
