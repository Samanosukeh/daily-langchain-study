```markdown
# Comentários passo a passo no Agent ReAct

## Visão Geral
O **ReAct** (Reasoning and Acting) é um padrão de agent que combina raciocínio (reasoning) e ação (acting) em um loop iterativo. Ele utiliza um modelo de linguagem para decidir qual ação tomar com base no contexto atual e no objetivo.

---

## Estrutura Básica do Agent ReAct

```python
from langchain.agents import AgentExecutor, initialize_agent
from langchain.agents.react.agent import ReActAgent
from langchain.tools import Tool

# 1. Definir ferramentas (Tools)
def buscar_preco_acao(símbolo: str) -> str:
    """Busca o preço atual de uma ação."""
    # Lógica de busca (ex: API, banco de dados, etc.)
    return f"Preço da ação {símbolo}: R$ 150,00"

ferramenta_acao = Tool(
    name="BuscarPreçoAção",
    func=buscar_preco_acao,
    description="Útil para buscar o preço atual de uma ação."
)

# 2. Inicializar o Agent ReAct
agent = ReActAgent.from_tools(
    tools=[ferramenta_acao],
    llm=llm,  # Modelo de linguagem (ex: ChatOpenAI)
    verbose=True  # Ativa logs detalhados
)

# 3. Executar o Agent
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=[ferramenta_acao],
    verbose=True
)

# 4. Rodar o Agent com uma consulta
response = agent_executor.run("Qual é o preço da ação PETR4?")
print(response)
```

---

## Fluxo de Execução do ReAct

1. **Entrada do Usuário**:
   - O agent recebe uma consulta (ex: "Qual é o preço da ação PETR4?").

2. **Raciocínio (Reasoning)**:
   - O modelo de linguagem analisa a consulta e planeja a próxima ação.
   - Exemplo de pensamento:
     ```
     "Preciso buscar o preço da ação PETR4. Vou usar a ferramenta 'BuscarPreçoAção' com o argumento 'PETR4'."
     ```

3. **Ação (Acting)**:
   - O agent executa a ferramenta selecionada (`BuscarPreçoAção`).
   - A ferramenta retorna o resultado (ex: "Preço da ação PETR4: R$ 150,00").

4. **Feedback e Iteração**:
   - O agent recebe o resultado e decide se precisa de mais ações ou se pode responder ao usuário.
   - Se necessário, repete os passos 2 e 3.

5. **Resposta Final**:
   - O agent retorna a resposta final ao usuário.

---

## Exemplo de Logs Detalhados (verbose=True)

```plaintext
> Entrada: Qual é o preço da ação PETR4?
> Thought: Preciso buscar o preço da ação PETR4. Vou usar a ferramenta 'BuscarPreçoAção' com o argumento 'PETR4'.
> Action: BuscarPreçoAção
> Action Input: {"símbolo": "PETR4"}
> Observation: Preço da ação PETR4: R$ 150,00
> Thought: Recebi o preço da ação. Posso responder ao usuário.
> Final Answer: O preço atual da ação PETR4 é R$ 150,00.
```

---

## Personalização do Agent ReAct

### 1. Adicionar Múltiplas Ferramentas
```python
def buscar_noticias_empresa(empresa: str) -> str:
    """Busca notícias recentes sobre uma empresa."""
    return f"Notícias sobre {empresa}: ... (exemplo de resposta)"

ferramenta_noticias = Tool(
    name="BuscarNotíciasEmpresa",
    func=buscar_noticias_empresa,
    description="Útil para buscar notícias recentes sobre uma empresa."
)

agent = ReActAgent.from_tools(
    tools=[ferramenta_acao, ferramenta_noticias],
    llm=llm,
    verbose=True
)
```

### 2. Personalizar o Modelo de Linguagem
```python
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,  # Controla a criatividade das respostas
    max_tokens=2000