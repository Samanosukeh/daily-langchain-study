```markdown
# Retriever Básico: Similarity Search em LangChain

## Instalação
```bash
pip install langchain pypdf sentence-transformers chromadb
```

## Carregar Documentos
```python
from langchain.document_loaders import PyPDFLoader

loader = PyPDFLoader("documento.pdf")
docs = loader.load()
```

## Dividir Documentos
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
split_docs = splitter.split_documents(docs)
```

## Embeddings
```python
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
```

## Vector Store
```python
from langchain.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    documents=split_docs,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
```

## Retriever
```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)
```

## Busca por Similaridade
```python
query = "Qual é o tema principal do documento?"
docs_relevantes = retriever.get_relevant_documents(query)

for doc in docs_relevantes:
    print(doc.page_content)
    print("---")
```

## Salvando o Vector Store
```python
vectorstore.persist()
```

## Carregando o Vector Store Existente
```python
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)
```

## Dica Extra
- Para modelos menores, use `all-MiniLM-L6-v2`.
- Ajuste `chunk_size` e `chunk_overlap` conforme o conteúdo.
- Para buscas híbridas, use `search_type="mmr"` (Maximal Marginal Relevance).
```