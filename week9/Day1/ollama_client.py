import requests 


ollama_url = "http://localhost:11434/api/generate"
Model_name = "tinyllama"


def call_llm(prompt: str, max_tokens: int= 300) -> str :
    reponse = requests.post(
        ollama_url,
        json={
            "model":Model_name,
            "prompt": prompt,
            "stream":False,
            "options":{
                "temperature":0.2,
                "num_predict":max_tokens
            }


        },

        timeout=120



    )
    reponse.raise_for_status()
    return reponse.json()["response"].strip()

