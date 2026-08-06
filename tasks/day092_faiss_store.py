```python
# tasks/day092_faiss_vector_store.py
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# 1. Dados de exemplo (substitua pela sua fonte real)
textos = [
    "O LangChain é uma biblioteca para desenvolvimento de aplicações com LLMs.",
    "FAISS é uma biblioteca para busca eficiente de vetores em alta dimensão.",
    "RAG combina recuperação de informações com geração de linguagem.",
    "O HuggingFace Embeddings converte texto em vetores numéricos."
]

# 2. Divisão dos textos em chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=10
)
docs = [Document(page_content=texto) for texto in textos]
splits = text_splitter.split_documents(docs)

# 3. Embeddings (usando modelo pré-treinado)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

# 4. Criação do Vector Store local com FAISS
vector_store = FAISS.from_documents(
    documents=splits,
    embedding=embeddings
)

# 5. Salvando o vector store para uso futuro
vector_store.save_local("faiss_index")

# 6. Carregando o vector store salvo (opcional)
loaded_vector_store = FAISS.load_local(
    "faiss_index",
    embeddings=embeddings,
    allow_dangerous_deserialization=True  # Necessário para versões recentes
)

# 7. Exemplo de busca semântica
query = "O que é RAG?"
docs_relevantes = loaded_vector_store.similarity_search(query, k=2)
print(f"Documentos relevantes para '{query}':")
for doc in docs_relevantes:
    print(f"- {doc.page_content}")
```

---

```markdown
# Comentários nos Loaders e Vector Stores

## Visão Geral
No contexto de RAG (Retrieval-Augmented Generation), os **loaders** e **vector stores** são componentes essenciais para ingestão e recuperação de dados. Comentários nesses componentes são fundamentais para:
- Documentar configurações.
- Explicar transformações de dados.
- Facilitar manutenção e debugging.

---

## 1. Loaders (Carregadores de Dados)

### Exemplo: `TextLoader` com Comentários
```python
from langchain.document_loaders import TextLoader

# Carrega um arquivo de texto simples.
# Parâmetros:
#   - file_path: Caminho para o arquivo de texto.
loader = TextLoader(file_path="dados/texto_exemplo.txt")

# Carrega o conteúdo do arquivo em um formato processável pelo LangChain.
# Retorna uma lista de `Document` (objetos que contêm `page_content` e `metadata`).
docs = loader.load()

# Exemplo de saída:
# [
#   Document(page_content="Conteúdo do arquivo...", metadata={"source": "dados/texto_exemplo.txt"})
# ]
```

### Comentários Relevantes
- **Configurações**: Documentar parâmetros como `file_path` ou `encoding`.
- **Saídas Esperadas**: Explicar o formato dos dados retornados (ex.: `Document`).
- **Tratamento de Erros**: Comentar casos como arquivos não encontrados ou permissões.

---

## 2. Vector Stores

### Exemplo: `FAISS` com Comentários
```python
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Inicializa um embedder usando o modelo 'sentence-transformers/all-MiniLM-L6-v2'.
# Parâmetros:
#   - model_name: Nome do modelo de embeddings.
#   - model_kwargs: Configurações adicionais (ex.: dispositivo de execução).
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Cria um Vector Store (FAISS) a partir de documentos.
# Parâmetros:
#   - documents: Lista de documentos (`Document`) para indexar.
#   - embedding_function: Função de embeddings para converter texto em vetores.
vector_store = FAISS.from_documents(documents=docs, embedding=embeddings)

# Salva o índice FAISS em disco para persistência.
vector_store.save_local("indices/faiss_index")

# Carrega o índice salvo para reutilização.
vector_store = FAISS.load_local("indices/faiss_index", embeddings)
```

### Comentários Relevantes
- **Modelos de Embeddings**: Documentar o modelo usado e sua versão.
- **Persistência**: Explicar o propósito de salvar/carregar índices (ex.: performance, reutilização).
- **Parâmetros de Busca**: Comentar opções como `k` (número de resultados) em métodos como `similarity_search`.

---

## 3. Boas Práticas para Comentários

### Em Loaders
```python
# Carrega documentos de um arquivo JSON.
# - file_path: Caminho para o arquivo JSON.
# - jq_schema: Filtro JQ para extrair campos específicos (ex.: ".data[]").
loader = JSONLoader(
    file_path="dados/dados.json",
    jq_schema=".data[]",  # Extrai cada item do array "data".
    text_content=False,   # Desativa o uso de texto bruto como conteúdo.
)
```

### Em Vector Stores
```python
# Busca os 5 documentos mais similares a uma consulta.
# - query: Texto da consulta.
# - k: Número de resultados a retornar (padrão: 4).
resultados = vector_store.similarity_search(query="Qual é o tema principal?", k=5)

# Adiciona novos documentos ao índice existente.
# - documents: Lista de documentos a serem adicionados.
vector_store.add_documents(documents=novos_docs)
```

---

## 4. Ferramentas Relacionadas
- **Loaders**:
  - `TextLoader`, `JSONLoader`, `PyPDFLoader`, `WebBaseLoader`.
- **Vector Stores**:
  - `FAISS`, `Chroma`, `Pinecone`, `Weaviate`.
- **Embeddings**:
  - `HuggingFaceEmbeddings`, `OpenAIEmbeddings`.

---

## 5. Referências
- [LangChain Documentation: Document Loaders](https://python.langchain.com/docs/modules/data_connection/document_loaders/)
- [LangChain Documentation: Vector Stores](