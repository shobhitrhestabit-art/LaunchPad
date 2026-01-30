import ollama
import logging
import time

logger = logging.getLogger(__name__)

class Llama3Agent:
    def __init__(self, model="llama3:7b-instruct-q4_K_M"):
        self.model = model
        self.max_retries = 3
        self.retry_delay = 2
        
        # Test connection on init
        self._test_connection()
    
    def _test_connection(self):
        
        try:
            logger.info(f"Testing connection to Ollama with model: {self.model}")
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': 'hi'}],
                stream=False
            )
            logger.info("✓ Ollama connection successful")
        except Exception as e:
            logger.error(f"✗ Cannot connect to Ollama: {e}")
            logger.error("Make sure to run: ollama serve")
            raise RuntimeError(
                "Ollama is not running. "
                "Start it with: 'ollama serve' in another terminal"
            )

    def chat(self, user_query, session_context, retrieved_context):
        """
        Generate response with context sandwich
        
        Args:
            user_query: Current user input
            session_context: Recent conversation history
            retrieved_context: Similar past interactions
        
        Returns:
            Response text or error message
        """
        try:
            # Create the 'Context Sandwich'
            system_prompt = f"""You are an AI assistant with access to long-term and short-term memory.

RELEVANT PAST MEMORIES:
{retrieved_context}

RECENT CONVERSATION:
{session_context}

Instructions:
- Use the context to provide consistent, informed responses
- If context contradicts new information, acknowledge the inconsistency
- Keep responses concise (under 150 words) for CPU efficiency
- If you don't know something, say so clearly"""
            
            logger.info(f"Sending query to Ollama: {user_query[:50]}...")
            
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_query},
                ],
                stream=False,
                options={
                    'temperature': 0.7,
                    'top_k': 40,
                    'top_p': 0.9,
                }
            )
            
            content = response['message']['content']
            logger.info(f"Response received ({len(content)} chars)")
            return content
            
        except ConnectionError as e:
            logger.error(f"Connection error: {e}")
            return (
                "LLM Error: Cannot connect to Ollama. "
                "Please start Ollama with: 'ollama serve'"
            )
        except KeyError as e:
            logger.error(f"Unexpected response format: {e}")
            return "LLM Error: Unexpected response format from Ollama"
        except Exception as e:
            logger.error(f"LLM error: {e}", exc_info=True)
            return f"LLM Error: {str(e)}"