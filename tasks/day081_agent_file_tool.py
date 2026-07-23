```python
from langchain.agents import AgentExecutor, initialize_agent
from langchain.agents import Tool
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# Ferramenta personalizada para escrita em arquivo
def write_to_file(content: str, filename: str) -> str:
    """Escreve conteúdo em um arquivo especificado."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        return f"Arquivo '{filename}' salvo com sucesso."
    except Exception as e:
        return f"Erro ao salvar arquivo: {str(e)}"

# Configuração do LLM (usando Ollama local)
llm = Ollama(model="llama3")

# Template de prompt para o agent
prompt_template = PromptTemplate.from_template(
    """Você é um assistente especializado em criar tarefas.
    {input}
    """
)

# Inicialização do agent com a ferramenta de escrita
tools = [
    Tool(
        name="Escritor de Arquivos",
        func=write_to_file,
        description="Útil para salvar tarefas ou informações em arquivos. "
                   "Parâmetros: content (conteúdo a ser salvo), filename (nome do arquivo)."
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Execução do agent com uma tarefa de exemplo
task = "Crie um arquivo chamado 'tasks/day_2024_05_20.txt' com o conteúdo: 'Revisar documentação do LangChain'"

try:
    result = agent.run(task)
    print("\nResultado:", result)
except Exception as e:
    print(f"Erro na execução: {str(e)}")
```