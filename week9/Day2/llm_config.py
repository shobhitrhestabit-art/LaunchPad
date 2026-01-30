


config_list = [
    {
        "model": "mistral:latest",                         
        "base_url": "http://localhost:11434/v1",    
        "api_key": "ollama",                        
    }
]

# Shared LLM configuration object
llm_config = {
    "config_list": config_list,
    "temperature": 0.2,    
    "timeout": 1200,        
}
