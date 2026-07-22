```python
from langchain.agents import AgentExecutor, initialize_agent
from langchain.llms import OpenAI

# Configuração mínima
llm = OpenAI(temperature=0)
tools = [...]  # Suas tools aqui

# Agent básico
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Debug simples
try:
    result = agent.run("Resolva a tarefa X com a ferramenta Y")
    print("Resultado:", result)
except Exception as e:
    print(f"Erro: {e}")
    print("\nDebug:")
    print(f"- Agent: {agent.agent}")
    print(f"- Tools: {agent.tools}")
    print(f"- Input: {agent.input_keys}")
```