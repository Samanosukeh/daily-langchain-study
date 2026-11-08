```python
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_mcp_adapters.client import MCPClient
from langchain_mcp_adapters.tools import MCPTool

# Configuração do cliente MCP
mcp_client = MCPClient(
    server_command=["python", "-m", "mcp.server.example"],
    server_env={"PYTHONPATH": "/caminho/para/seu/servidor/mcp"},
)

# Inicialização das tools do MCP
mcp_tools = mcp_client.get_tools()

# Conversão das tools MCP para tools LangChain
tools = [
    MCPTool(
        name=tool.name,
        description=tool.description,
        args_schema=tool.args_schema,
        func=tool.func,
    )
    for tool in mcp_tools
]

# Definição do prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente especializado em tarefas técnicas que usa ferramentas de servidor MCP."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Criação do agente
agent = create_tool_calling_agent(
    llm=llm,  # Substitua pelo seu modelo de linguagem (ex: ChatOpenAI)
    tools=tools,
    prompt=prompt,
)

# Criação do executor do agente
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)

# Exemplo de execução
if __name__ == "__main__":
    chat_history = []

    while True:
        user_input = input("Digite sua tarefa (ou 'sair' para encerrar): ")
        if user_input.lower() == "sair":
            break

        result = agent_executor.invoke({
            "input": user_input,
            "chat_history": chat_history,
        })

        chat_history.extend([
            HumanMessage(content=user_input),
            AIMessage(content=result["output"]),
        ])

        print("\nResultado:", result["output"], "\n")
```