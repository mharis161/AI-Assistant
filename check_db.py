
from vector_store import VectorStore
import sys

def check_database_content():
    print("Checking database content...")
    try:
        vs = VectorStore()
        # Get all metadata
        result = vs.collection.get()
        metadatas = result['metadatas']
        
        if not metadatas:
            print("Database is empty.")
            return

        # Extract unique filenames
        filenames = set()
        for m in metadatas:
            if m and 'filename' in m:
                filenames.add(m['filename'])
        
        print("\nFiles currently in Vector Database:")
        print("-" * 30)
        for f in filenames:
            print(f"• {f}")
        print("-" * 30)
        print(f"Total chunks: {len(metadatas)}")
        
    except Exception as e:
        print(f"Error checking database: {e}")

if __name__ == "__main__":
    check_database_content()
