we will use the ollama server , and download the Tinyllama 

TInyllama serve the model on the localhost:11434

check the models -->  ollama list 

ollama run <model-name>


we will use the ollama mistral 7B ,for the Day1


we run the models using 

we need to create 3 independent agents ,and the user will write a prompt

user prompt ---> Research agent(Gather information  using  mistral ) send the response to ---> summarize agent(Summarize the answers using llm  )send response to ----> answer agents (it will make the answer out of the summary using the llm mistral and present it to the output ).


we will use the mistral using ollama server 11434 port  ,running .





we will make a query.py to take the user input 

we will make the load_llm.py to load the llm 



### Inside the  ollama 

