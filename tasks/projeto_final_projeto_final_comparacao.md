```markdown
# Projeto Final: Agent de Q&A com LangChain

## Comparação entre Abordagens

### 1. **Agent com Ferramentas Externas (Google Search + Wikipedia)**
```python
from langchain.agents import initialize_agent, Tool
from langchain.utilities import GoogleSearchAPIWrapper, WikipediaAPIWrapper

search = GoogleSearchAPIWrapper()
wiki = WikipediaAPIWrapper()

tools = [
    Tool(
        name="Google Search",
        func=search.run,
        description="Busca na web por informações atualizadas."
    ),
    Tool(
        name="Wikipedia",
        func=wiki.run,
        description="Busca em artigos da Wikipedia."
    )
]

agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)
```
**Prós:**
- Respostas atualizadas (Google).
- Fontes confiáveis (Wikipedia).
- Flexível para domínios amplos.

**Contras:**
- Custo com APIs externas.
- Latência em buscas múltiplas.

---

### 2. **Agent com Base de Conhecimento Local (PDFs + Vector Store)**
```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# Carregar e dividir documentos
loader = PyPDFLoader("documento.pdf")
pages = loader.load_and_split()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(pages)

# Criar vetor store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
db = Chroma.from_documents(texts, embeddings)

# Agent com retriever
retriever = db.as_retriever(search_kwargs={"k": 3})
qa_agent = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)
```
**Prós:**
- Sem custos externos.
- Respostas precisas para domínios específicos.
- Controle total sobre os dados.

**Contras:**
- Manutenção da base de conhecimento.
- Menos atualizado para tópicos dinâmicos.

---
### 3. **Agent Híbrido (Local + Ferramentas Externas)**
```python
tools = [
    Tool(
        name="Documentos Locais",
        func=qa_agent.run,
        description="Responde com base em documentos internos."
    ),
    Tool(
        name="Google Search",
        func=search.run,
        description="Busca na web por informações complementares."
    )
]

hybrid_agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)
```
**Prós:**
- Combina precisão e atualização.
- Ideal para domínios com fontes próprias + internet.

**Contras:**
- Complexidade aumentada.
- Custo elevado se depender de APIs.

---
## Recomendação Final
- **Domínios estáticos:** Base de conhecimento local.
- **Informações dinâmicas:** Ferramentas externas.
- **Equilíbrio:** Híbrido.
```