```markdown
# Lições aprendidas: 6 meses de LangChain

## Projeto Final

### Visão Geral
Após 6 meses de estudo e implementação com LangChain, este documento resume as principais lições aprendidas durante o desenvolvimento do projeto final.

---

## 1. Arquitetura do Projeto
### Estrutura de Pastas Recomendada
```plaintext
projeto_final/
│
├── src/
│   ├── agents/               # Definição de agentes personalizados
│   ├── chains/               # Encadeamentos de LLM
│   ├── tools/                # Ferramentas customizadas
│   ├── utils/                # Funções auxiliares
│   └── main.py               # Ponto de entrada da aplicação
│
├── data/                     # Dados de entrada/saída
├── config/                   # Arquivos de configuração (YAML/JSON)
├── tests/                    # Testes unitários/integração
├── requirements.txt          # Dependências
└── README.md                 # Documentação do projeto
```

### Pontos-Chave
- **Separação de responsabilidades**: Agentes, chains e tools devem ser modulares.
- **Configuração centralizada**: Use arquivos `.env` ou `config.yaml` para parâmetros sensíveis.
- **Logging estruturado**: Implemente logs para depuração (ex: `structlog` ou `loguru`).

---

## 2. Integração com LLMs
### Melhores Práticas
1. **Escolha do Modelo**:
   - Para tarefas de geração: `gpt-3.5-turbo`, `gpt-4`, ou modelos open-source como `llama2`.
   - Para tarefas de classificação: Modelos menores como `distilbert`.

2. **Parâmetros de Configuração**:
   ```python
   from langchain.llms import HuggingFaceHub

   llm = HuggingFaceHub(
       repo_id="google/flan-t5-large",
       model_kwargs={"temperature": 0.5, "max_length": 1024}
   )
   ```

3. **Cache de Respostas**:
   - Use `InMemoryCache` para evitar chamadas repetidas ao LLM:
     ```python
     from langchain.cache import InMemoryCache
     from langchain.globals import set_llm_cache

     set_llm_cache(InMemoryCache())
     ```

---

## 3. Criação de Agents
### Customização de Agents
- **AgentExecutor**: Gerencie o fluxo de execução do agente.
- **Tools**: Integre APIs externas ou funções Python como ferramentas.

Exemplo:
```python
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

def buscar_dados_api(query: str) -> str:
    # Lógica para buscar dados de uma API
    return "Dados retornados"

tools = [
    Tool(
        name="BuscarDadosAPI",
        func=buscar_dados_api,
        description="Útil para buscar dados de uma API externa"
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

response = agent.run("Busque dados sobre o projeto final")
print(response)
```

### Lições
- **Descrições claras das tools**: A descrição deve ser precisa para o agente entender quando usá-las.
- **Validação de inputs**: Sempre valide os inputs das tools para evitar erros.

---

## 4. Encadeamento de Chains
### Tipos de Chains
1. **SimpleSequentialChain**: Executa chains em sequência.
   ```python
   from langchain.chains import SimpleSequentialChain

   chain1 = prompt_template_1 | llm
   chain2 = prompt_template_2 | llm

   overall_chain = SimpleSequentialChain(
       chains=[chain1, chain2],
       verbose=True
   )
   ```

2. **RetrievalQA**: Para perguntas sobre documentos.
   ```python
   from langchain.chains import RetrievalQA
   from langchain.vectorstores import FAISS
   from langchain.embeddings import HuggingFaceEmbeddings

   embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
   db = FAISS.from_documents(documents, embeddings)

   qa_chain = RetrievalQA.from_chain_type(
       llm=llm,
       chain_type="stuff",
       retriever=db.as_retriever()
   )
   ```

### Lições
-