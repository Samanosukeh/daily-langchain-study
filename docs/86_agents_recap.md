```markdown
# Resumo Mês 2.5: Agents Completos

## Visão Geral

Neste estágio, foi implementado **Agents Completos** no LangChain, integrando múltiplas ferramentas, raciocínio dinâmico e execução autônoma de tarefas complexas.

---

## Estrutura do Agent Completo

### 1. **Definição do Agent**
```python
from langchain.agents import AgentExecutor, initialize_agent
from langchain.llms import OpenAI
from langchain.agents import Tool

# Inicialização do LLM
llm = OpenAI(temperature=0)

# Ferramentas (tools) disponíveis
tools = [
    Tool(
        name="Calculadora",
        func=lambda x: str(eval(x)),  # Exemplo simples (substituir por implementação segura)
        description="Útil para cálculos matemáticos."
    ),
    Tool(
        name="Busca na Web",
        func=web_search_tool,  # Função externa para busca
        description="Busca informações na internet."
    )
]

# Inicialização do Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",  # Tipo de agent
    verbose=True
)
```

---

### 2. **Executor do Agent**
```python
# Execução de tarefas
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True
)

# Chamada do agent
response = agent_executor.run("Calcule 15% de 200 e pesquise sobre IA generativa.")
print(response)
```

---

## Componentes-Chave

### 1. **Ferramentas (Tools)**
- **Definição**: Funções acionáveis que o agent pode usar.
- **Exemplos**:
  - Busca na web (`SerpAPI`, `Tavily`).
  - Acesso a APIs externas (`requests`).
  - Funções locais (cálculos, manipulação de dados).

### 2. **Prompt Template**
```python
from langchain.prompts import PromptTemplate

template = """Responda à seguinte pergunta o mais detalhadamente possível.
Pergunta: {input}
Histórico: {history}
Resposta:"""

prompt = PromptTemplate(
    input_variables=["input", "history"],
    template=template
)
```

### 3. **Memory (Memória)**
```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="history",
    return_messages=True
)
```

### 4. **Agent Types**
- **`zero-shot-react-description`**: Baseado em descrições de ferramentas (recomendado para início).
- **`react-docstore`**: Para agentes com acesso a documentos.
- **`self-ask-with-search`**: Para busca iterativa em múltiplas fontes.

---

## Exemplo Prático: Agent de Pesquisa + Cálculo

```python
from langchain.agents import load_tools

# Carregar ferramentas prontas (ex: busca na web)
tools = load_tools(["serpapi", "llm-math"], llm=llm)

# Inicializar agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Execução
agent.run("Quanto foi o PIB do Brasil em 2023? Calcule 10% desse valor.")
```

---

## Boas Práticas

1. **Validação de Ferramentas**:
   - Garanta que as funções das ferramentas sejam seguras (ex: evitar `eval` em produção).
   - Use bibliotecas como `numexpr` para cálculos matemáticos.

2. **Prompt Engineering**:
   - Inclua exemplos no `PromptTemplate` para guiar o agent.
   - Defina limites claros na descrição das ferramentas.

3. **Monitoramento**:
   - Ative `verbose=True` para debugar interações.
   - Logue as chamadas de ferramentas e respostas.

4. **Otimização**:
   - Cache de resultados de buscas (ex: `TTLCache`).
   - Limite de tokens para evitar custos excessivos.

---

## Arquivos Relevantes

- **`docs/agents/completos/agent_executor.py`**: Implementação base.
- **`docs/agents/completos/tools/`**: Ferramentas customizadas.
- **`docs/agents/completos/memory/`**: Configurações de memória.

---
## Referências
- [LangChain Agents