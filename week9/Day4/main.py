import numpy as np
import os
import logging
from sentence_transformers import SentenceTransformer
from memory.session_memory import SessionMemory
from memory.vector_store import VectorStore
from utils.db_handler import DBHandler
from llm.llama_engine import Llama3Agent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create required directories
os.makedirs("memory", exist_ok=True)
os.makedirs("utils", exist_ok=True)


logger.info("Loading embedding model...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

logger.info("Initializing database...")
db = DBHandler()

logger.info("Initializing vector store...")
vector_memory = VectorStore(dimension=384)

logger.info("Initializing session memory...")
session = SessionMemory(n=5)

logger.info("Initializing Llama3 agent...")

llama = Llama3Agent(model="llama3:latest")

logger.info("Agent initialized successfully!")

def run_agent_workflow(user_query):
    """
    Main workflow: vectorize → search → retrieve → augment → respond → persist
    """
    try:
        
        if not user_query or not user_query.strip():
            logger.warning("Empty query received")
            return "Please provide a valid query."
        
        print(f"\n--- Processing Query: {user_query} ---")
        
        
        logger.info("Encoding query...")
        query_vector = embedder.encode(user_query)
        
        
        logger.info("Searching vector store...")
        similar_ids = vector_memory.search(query_vector, k=3)
        logger.info(f"Found similar IDs: {similar_ids}")
        
        
        logger.info("Retrieving context from database...")
        if similar_ids and similar_ids[0] != -1:
            retrieved_context = db.get_text_by_ids(similar_ids)
        else:
            logger.info("No similar memories found (cold start)")
            retrieved_context = "No prior memories found yet."
        
       
        logger.info("Getting session context...")
        session_context = session.get_context_string()
        if not session_context:
            session_context = "No recent conversation history."
        
       
        logger.info("Generating response from LLM...")
        response = llama.chat(user_query, session_context, retrieved_context)
        logger.info("Response generated successfully")
        
        # STEP 6: Persistence (The Storage Flow)
        # A. Save the interaction text to SQLite and get the new unique ID
        logger.info("Saving interaction to database...")
        interaction_text = f"User: {user_query} | AI: {response}"
        new_id = db.save_text(interaction_text)
        logger.info(f"Saved with ID: {new_id}")
        
        # B. Save the vector to FAISS using that SAME SQLite ID
        logger.info("Adding vector to FAISS...")
        vector_memory.add_vector(query_vector, new_id)
        
        # C. Update the RAM-based session memory
        logger.info("Updating session memory...")
        session.add_message("user", user_query)
        session.add_message("assistant", response)
        
        logger.info("Workflow completed successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error in workflow: {e}", exc_info=True)
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Local Llama3 Agent with Memory System")
    print("="*60)
    print("\nAgent is ready. Type 'exit' or 'quit' to exit.")
    print("NOTE: First response may take 10-30 seconds on CPU\n")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                print("Please enter a query.")
                continue
            
            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye!")
                break
            
            answer = run_agent_workflow(user_input)
            print(f"\nLlama 3: {answer}")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            print(f"Unexpected error: {e}")