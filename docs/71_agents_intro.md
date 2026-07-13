```markdown
# Agents em LangChain: ReAct e o Ciclo Thought-Action-Obs

## Introdução
Agents em LangChain são componentes que utilizam modelos de linguagem para tomar decisões dinâmicas, interagir com ferramentas e executar tarefas complexas. O padrão **ReAct** (Reasoning and Acting) é um framework que define um ciclo iterativo de **Thought-Action-Observation** para guiar o comportamento do agent.

---

## Ciclo Thought-Action-Observation
O ciclo **Thought-Action-Obs** é o coração do ReAct, onde o agent:
1. **Thought (Pensamento)**: Analisa o contexto atual e planeja a próxima ação.
2. **Action (Ação)**: Executa uma ação (ex.: chamar uma ferramenta, buscar dados).
3. **Observation (Observação)**: Processa o resultado da ação para ajustar o plano.

### Fluxo Básico
```plaintext
Input → Thought → Action → Observation → Thought → ... → Final Answer
```

---

## Implementação com LangChain
### 1. Configuração do Agent
```python
from langchain.agents import AgentExecutor, initialize_agent
from langchain.agents import load_tools
from langchain.llms import OpenAI

# Carregar modelo de linguagem
llm = OpenAI(temperature=0)

# Carregar ferramentas (ex.: busca na web, calculadora)
tools = load_tools(["serpapi", "llm-math"], llm=llm)

# Inicializar agent com ReAct
agent = initialize_agent(
    tools,
    llm,
    agent="react-docstore",  # ou "zero-shot-react-description"
    verbose=True,
)
```

### 2. Execução do Ciclo
```python
# Executar agent com uma pergunta
response = agent.run("Quanto é 20% de 150?")
print(response)
```

---

## Exemplo de Saída (ReAct)
```plaintext
Thought: Preciso calcular 20% de 150.
Action: Calculator (20% * 150)
Observation: 30
Thought: O resultado é 30.
Final Answer: 30
```

---

## Variações de Agents
| Tipo de Agent | Descrição |
|---------------|-----------|
| `zero-shot-react-description` | Usa descrições das ferramentas para planejar ações. |
| `react-docstore` | Otimizado para interagir com documentos (ex.: busca em bancos de dados). |
| `self-ask-with-search` | Agent que faz perguntas de follow-up antes de responder. |

---

## Melhores Práticas
1. **Ferramentas Claras**: Defina ferramentas com descrições precisas para o agent.
2. **Verbose Mode**: Habilite `verbose=True` para debugar o ciclo Thought-Action-Obs.
3. **Feedback Loop**: Use `Observation` para ajustar ações futuras (ex.: retry em erros).

---

## Referências
- [Documentação Oficial de Agents em LangChain](https://python.langchain.com/docs/modules/agents/)
- Paper ReAct: [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
```