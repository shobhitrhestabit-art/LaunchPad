### Day2 

Orchestration is like the managing block ,which manages the agetns .

Multiple Archestration patterns -- 

when we use multiple agents , we assign each tasks to a dedicated ai in human teamwork .using multiple agents provides several advantages compared to monlithic single-agent solutions .


Benefits -- 
specialization 
scalability
Maintainability
Optimization 


Sequential orchestration 

Sequential orchestration pattern chains ai agents in a predefined,linear order. Each agent   processes the output from the previous agent  in the sequence .

Progressive refinement , this pattern resembles the Pipes and Filters

Which agent get invoked is defined as a part of the workflow and isnt a choice given to agetns in the process .


Concurrent Orchestration 

The concurrent orchestration pattern runs multiple ai agents simultaneously on teh same task . This approach allows each agent to provide independent  analysis on processing from its unique perspective or specialization .


user query -- > UserProxyAgent sent query to planner agent .



User sends a request → Planner decomposes it into tasks → tasks are sent to worker agents → worker agents execute tasks (in parallel) → their responses are gathered → then reflection and validation happen → final answer is produced.



### User sends a request → Planner decomposes it into tasks → tasks are sent to worker agents → worker agents execute tasks (in parallel) → their responses are gathered → then reflection and validation happen → final answer is produced.



Tasks are created based on independent reasoning units, not sentence count or agent count.



### WORKFLOW

1.We take the query from the user .
2.Now UserProxyAgent of the Autogen send the query to planner.
3.Now planner takes the query ,create multiple taks ,which are independent of each other .
4.from 1 query ,it makes multiple tasks,
5.Worker agent(paralellism)  - read the tasks,reasons about the tasks,calls llm , generates a task request ,sends the result back to the orchestrator .
6.Reflection Agent - Reads all the worker output together, finds any overlaps,Missing transition,Redundant explanations .

7.Validation Agent  ---- > Approved || Rejected



### Too slow 

Parallel working of 
