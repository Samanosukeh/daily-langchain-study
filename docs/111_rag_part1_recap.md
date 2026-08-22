```markdown
# Resumo RAG Parte 1: Embeddings, Stores e Retrievers

## Introdução ao RAG (Retrieval-Augmented Generation)

O RAG é uma técnica que combina recuperação de informações com geração de linguagem natural para melhorar a qualidade das respostas em modelos de linguagem. Aqui focamos nos componentes essenciais de um pipeline RAG.

---

## 1. Embeddings

### O que são?
Vetores numéricos que representam semanticamente textos, capturando seu significado em um espaço contínuo.

### Principais características:
- **Dimensionalidade**: Geralmente 768, 1024 ou 1536 dimensões (dependendo do modelo).
- **Similaridade**: Usam cosseno ou distância euclidiana para medir semelhança.
- **Modelos populares**:
  - `text-embedding-ada-002` (OpenAI)
  - `sentence-transformers/all-MiniLM-L6-v2` (Hugging Face)
  - `BAAI/bge-small-en` (BAAI)

### Exemplo de uso em Python:
```python
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
text = "O RAG melhora a geração de texto com recuperação de informações."
embedding = embeddings.embed_query(text)
print(len(embedding))  # Output: 384 (dimensões do modelo)
```

---

## 2. Vector Stores (Armazenamento de Vetores)

### O que são?
Bancos de dados especializados em armazenar e buscar embeddings com alta performance.

### Principais opções:
| Banco de Dados | Características | Biblioteca LangChain |
|----------------|-----------------|---------------------|
| **Chroma** | Leve, open-source, integrável | `Chroma` |
| **FAISS** | Otimizado para busca por similaridade | `FAISS` |
| **Pinecone** | Serviço gerenciado, escalável | `Pinecone` |
| **Weaviate** | GraphQL nativo, multi-modal | `Weaviate` |
| **Milvus** | Open-source, alta performance | `Milvus` |

### Exemplo de criação com Chroma:
```python
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader

loader = TextLoader("documento.txt")
documents = loader.load()
vectorstore = Chroma.from_documents(documents, embeddings)
```

---

## 3. Retrievers (Recuperadores)

### O que são?
Componentes que buscam os documentos mais relevantes com base em uma query.

### Tipos de retrievers:
1. **Vector Store Retriever**: Busca por similaridade vetorial.
   ```python
   retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
   docs = retriever.get_relevant_documents("O que é RAG?")
   ```

2. **Multi-Query Retriever**: Gera múltiplas queries para melhorar a cobertura.
   ```python
   from langchain.retrievers import MultiQueryRetriever
   retriever = MultiQueryRetriever.from_llm(
       vectorstore.as_retriever(), llm
   )
   ```

3. **Parent Document Retriever**: Recupera chunks pequenos mas retorna documentos completos.
   ```python
   from langchain.retrievers import ParentDocumentRetriever
   retriever = ParentDocumentRetriever(
       vectorstore=vectorstore,
       docstore=docstore,
       child_splitter=small_splitter,
       parent_splitter=large_splitter
   )
   ```

4. **Ensemble Retriever**: Combina múltiplos métodos de recuperação.
   ```python
   from langchain.retrievers import EnsembleRetriever
   retriever = EnsembleRetriever(
       retrievers=[vector_retriever, keyword_retriever],
       weights=[0.5, 0.5]
   )
   ```

---

## 4. Pipeline Básico RAG

1. **Indexação**:
   - Carregar documentos
   - Dividir em chunks
   - Gerar embeddings
   - Armazenar no vector store

2. **Recuperação**:
   - Receber query do usuário
   - Gerar embedding da query
   - Buscar documentos similares no vector store

3. **Geração**:
   - Combinar documentos recuperados com a query
   - Passar para o LLM para geração da resposta

### Exemplo completo:
```python
from langchain