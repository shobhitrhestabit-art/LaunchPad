import requests
import json

class Llama3Client:
    """
    Production-grade Llama-3 client using Ollama's local API.
    Bypasses subprocess permission and timeout issues.
    """

    def __init__(self, model: str = "llama3", timeout: int = 300):
        self.model = model
        self.timeout = timeout
        self.api_url = "http://localhost:11434/api/generate"
        print(f"[LLAMA3_CLIENT.__init__] Model: {model}, API: {self.api_url}")

    def generate(self, prompt: str) -> str:
        print(f"[LLAMA3_CLIENT.generate] Starting API inference...")
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
           
            response = requests.post(
                self.api_url, 
                json=payload, 
                timeout=self.timeout
            )
            
            
            response.raise_for_status()
            
            result = response.json()
            output = result.get("response", "").strip()

            if not output:
                raise RuntimeError("Empty response from Llama-3 API")

            print(f"[LLAMA3_CLIENT.generate]  Success ({len(output)} chars)")
            return output

        except requests.exceptions.Timeout:
            print(f"[LLAMA3_CLIENT.generate]  Timeout after {self.timeout}s")
            raise RuntimeError("Llama-3 inference timed out")
        
        except requests.exceptions.ConnectionError:
            print(f"[LLAMA3_CLIENT.generate]  Connection failed. Is Ollama running?")
            raise RuntimeError("Could not connect to Ollama server. Run 'ollama serve'")

        except Exception as e:
            print(f"[LLAMA3_CLIENT.generate]  Unexpected error: {e}")
            raise RuntimeError(f"Llama-3 API execution failed: {e}")