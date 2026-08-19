```python
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

# Dados de exemplo com metadados
documents = [
    Document(
        page_content="O Python é uma linguagem de programação de alto nível.",
        metadata={"source": "wikipedia", "category": "programming", "year": 2023}
    ),
    Document(
        page_content="LangChain é uma framework para desenvolvimento de aplicações com LLMs.",
        metadata={"source": "github", "category": "ai", "year": 2023}
    ),
    Document(
        page_content="O SQL é uma linguagem de consulta estruturada para bancos de dados.",
        metadata={"source": "wikipedia", "category": "database", "year": 2022}
    )
]

# Inicializa o vetor store com Chroma
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# Cria o retriever
retriever = vectorstore.as_retriever()

# Filtro por metadados (exemplo: category = "programming")
filtered_docs = retriever.invoke(
    "linguagem de programação",
    filter={"category": "programming"}
)

print("Documentos filtrados por metadados:")
for doc in filtered_docs:
    print(f"\nConteúdo: {doc.page_content}")
    print(f"Metadados: {doc.metadata}")

# Filtro por múltiplos critérios (exemplo: category = "ai" e year = 2023)
filtered_docs = retriever.invoke(
    "LLM",
    filter={"category": "ai", "year": 2023}
)

print("\nDocumentos filtrados por múltiplos metadados:")
for doc in filtered_docs:
    print(f"\nConteúdo: {doc.page_content}")
    print(f"Metadados: {doc.metadata}")
```