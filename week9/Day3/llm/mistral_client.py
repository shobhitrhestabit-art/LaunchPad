import requests
import json

class MistralClient:
    def __init__(self, model: str = "mistral", timeout: int = 300):
        self.model = model
        self.timeout = timeout
        self.api_url = "http://localhost:11434/api/generate"
        print(f"[MISTRAL_CLIENT] Initialized via API (Port 11434)")

    def generate(self, prompt: str) -> str:
        print(f"[MISTRAL_CLIENT.generate] Sending request to Ollama API...")
        
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
            
            data = response.json()
            output = data.get("response", "").strip()

            if not output:
                raise RuntimeError("Empty response from Mistral API")

            print(f"[MISTRAL_CLIENT.generate]  Success ({len(output)} chars)")
            return output

        except requests.exceptions.Timeout:
            print(" API Timeout: Ollama took too long to respond.")
            raise RuntimeError("Mistral inference timed out")
        except requests.exceptions.ConnectionError:
            print(" Connection Error: Is Ollama running? (Check 'ollama serve')")
            raise RuntimeError("Could not connect to Ollama server")
        except Exception as e:
            print(f" Unexpected error: {e}")
            raise RuntimeError(f"Mistral execution failed: {e}")