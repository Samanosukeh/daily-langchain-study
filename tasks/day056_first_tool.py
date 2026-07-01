```python
from langchain_core.tools import tool

@tool
def buscar_produto_por_id(id_produto: str) -> dict:
    """Busca um produto no banco de dados pelo ID.

    Args:
        id_produto: ID único do produto.

    Returns:
        Dicionário com os dados do produto ou mensagem de erro.
    """
    # Simulação de busca em banco de dados
    produtos = {
        "1": {"nome": "Notebook Gamer", "preco": 4500.00, "estoque": 10},
        "2": {"nome": "Mouse sem fio", "preco": 89.90, "estoque": 50},
    }

    return produtos.get(id_produto, {"erro": "Produto não encontrado"})

@tool
def calcular_desconto(valor: float, percentual: float) -> float:
    """Aplica um desconto percentual sobre um valor.

    Args:
        valor: Valor original.
        percentual: Percentual de desconto (0-100).

    Returns:
        Valor com desconto aplicado.
    """
    if percentual < 0 or percentual > 100:
        raise ValueError("Percentual deve estar entre 0 e 100")
    return valor * (1 - percentual / 100)

# Exemplo de uso
if __name__ == "__main__":
    print(buscar_produto_por_id("1"))
    print(calcular_desconto(100.0, 15.0))
```

---

```markdown
# Comentários: Como o LLM Decide Usar uma Tool

## Visão Geral
O LangChain gerencia a decisão de um LLM (Large Language Model) invocar uma ferramenta (tool) com base em dois componentes principais:
1. **Arquitetura do Agente (Agent Architecture)**
2. **Prompt de Sistema (System Prompt)**

---

## 1. Arquitetura do Agente
A decisão de usar uma tool é influenciada pela configuração do agente. Os principais tipos de agentes no LangChain são:

### **AgentExecutor**
- **Funcionamento**: O LLM recebe a saída de ferramentas e decide se continua a execução ou encerra.
- **Critério de Invocação**:
  - O LLM gera uma saída no formato `Action: <nome_da_tool>, Action Input: <argumentos>`.
  - O `AgentExecutor` intercepta essa saída e invoca a tool correspondente.
  - Após a execução, o resultado é injetado novamente no contexto do LLM para continuar a geração.

### **StructuredToolsAgent**
- **Funcionamento**: Usa um prompt estruturado para guiar o LLM a escolher tools com base em um schema definido.
- **Critério de Invocação**:
  - O LLM deve retornar uma resposta no formato JSON com `tool` e `tool_input`.
  - Exemplo:
    ```json
    {
      "tool": "search_tool",
      "tool_input": {"query": "previsão do tempo para São Paulo"}
    }
    ```

---

## 2. Prompt de Sistema (System Prompt)
O prompt de sistema é responsável por instruir o LLM sobre quando e como usar tools. Um exemplo básico:

```python
system_prompt = """
Você é um assistente útil que pode usar ferramentas para responder perguntas.

Ferramentas disponíveis:
- search_tool: Pesquisa informações na web.
- calculator_tool: Realiza cálculos matemáticos.

Formato de resposta:
- Se precisar de uma ferramenta, retorne:
  Action: <nome_da_tool>, Action Input: <argumentos>

- Se não precisar de uma ferramenta, responda normalmente.
"""
```

### **Elementos-Chave do Prompt**:
1. **Contexto**: Explicar o papel do assistente e as ferramentas disponíveis.
2. **Formato de Saída**: Definir como o LLM deve solicitar a invocação de uma tool.
3. **Regras de Decisão**: Instruir o LLM a usar tools apenas quando necessário.

---

## Fluxo de Decisão
1. **Entrada do Usuário**: O usuário faz uma pergunta ou comando.
2. **Geração do LLM**: O LLM analisa a entrada e decide se uma tool é necessária.
3. **Invocação da Tool**: Se uma tool for necessária, o LLM gera a ação no formato esperado.
4. **Execução da Tool**: O `AgentExecutor` ou `StructuredToolsAgent` invoca a tool com os argumentos fornecidos.
5. **Feedback para o LLM**: O resultado da tool é retornado ao LLM para continuar a geração ou finalizar a resposta.

---

## Exemplo Prático
### Código:
```python
from langchain.agents import AgentExecutor, initialize_agent
from langchain.llms import OpenAI
from langchain.tools import Tool

# Definir uma tool simples
def search_tool(query: str) -> str:
    return f"Resultado da busca por '{query}'."

# Inicializar o LLM
llm = OpenAI(temperature=0)

# Criar a tool
tool = Tool(
    name="search_tool",
    func=search_tool,
    description="Pesquisa informações na web."
)

# Inicializar o agente
agent = initialize_agent(
    tools=[tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Executar o agente
agent.run("Qual é a capital do Brasil?")
```

### Saída Esperada:
```
> Entrada do usuário: "Qual é a capital do Brasil?"
> LLM: "Action: search_tool, Action Input: {'query': 'capital do Brasil'}"

> Tool Invocada: search_tool("capital do Brasil")
> Resultado: "Resultado da busca por 'capital do Brasil'."

> LLM: "A capital do Brasil é Brasília."
```

---

## Considerações Finais
- **Personalização**: A decisão de usar uma tool depende fortemente do prompt de sistema e da arquitetura do agente.
- **Melhoria Contínua**: Ajuste o prompt e as ferr