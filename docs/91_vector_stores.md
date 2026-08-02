```markdown
# Vector Stores: o que são e opções disponíveis

## O que são Vector Stores?

Vector Stores são bancos de dados especializados no armazenamento e recuperação de **vetores de embeddings** (representações numéricas de dados como texto, imagens, etc.). Eles são essenciais em pipelines de **RAG (Retrieval-Augmented Generation)** para buscar informações relevantes com base em similaridade semântica.

### Características principais:
- **Armazenamento eficiente**: Vetores são indexados para buscas rápidas.
- **Similaridade semântica**: Usam métricas como **cosine similarity** ou **L2 distance** para recuperar dados próximos ao vetor de consulta.
- **Integração com LLMs**: Fornecem contexto para modelos de linguagem gerarem respostas mais precisas.

---

## Opções de Vector Stores disponíveis

### 1. **FAISS (Facebook AI Similarity Search)**
- **Desenvolvido por**: Meta (Facebook).
- **Tipo**: Biblioteca em C++ com bindings para Python.
- **Vantagens**:
  - Otimizado para performance em CPU/GPU.
  - Suporte a índices hierárquicos (HNSW), IVF, e outros.
- **Uso típico**:
  ```python
  import faiss
  index = faiss.IndexFlatL2(dimensao_do_vetor)  # L2 distance
  index.add(vetores)  # Adiciona vetores ao índice
  ```

### 2. **Chroma**
- **Tipo**: Banco de dados vetorial open-source.
- **Vantagens**:
  - Simples de usar, ideal para prototipação.
  - Persistência local ou em nuvem.
  - Integração nativa com LangChain.
- **Exemplo de uso**:
  ```python
  from langchain.vectorstores import Chroma
  db = Chroma.from_documents(documentos, embeddings)
  resultados = db.similarity_search("consulta")
  ```

### 3. **Pinecone**
- **Tipo**: Serviço gerenciado (SaaS).
- **Vantagens**:
  - Escalabilidade automática.
  - Suporte a filtros métricos e metadados.
- **Exemplo**:
  ```python
  from pinecone import Pinecone
  pc = Pinecone(api_key="SUA_CHAVE")
  index = pc.Index("nome-do-indice")
  ```

### 4. **Weaviate**
- **Tipo**: Banco de dados vetorial open-source ou gerenciado.
- **Vantagens**:
  - Suporte a **GraphQL** para consultas avançadas.
  - Módulos de classificação e agrupamento.
- **Exemplo**:
  ```python
  from weaviate import Client
  client = Client("http://localhost:8080")
  ```

### 5. **Milvus / Zilliz**
- **Tipo**: Banco de dados vetorial open-source (Milvus) ou gerenciado (Zilliz).
- **Vantagens**:
  - Suporte a **GPU** para buscas rápidas.
  - Escalabilidade horizontal.
- **Exemplo**:
  ```python
  from pymilvus import Collection
  collection = Collection("nome-da-colecao")
  ```

### 6. **Qdrant**
- **Tipo**: Banco de dados vetorial open-source.
- **Vantagens**:
  - Filtragem por payload (metadados).
  - Suporte a **HNSW** e outros algoritmos.
- **Exemplo**:
  ```python
  from qdrant_client import QdrantClient
  client = QdrantClient("localhost", port=6333)
  ```

### 7. **Redis (com módulo RedisSearch)**
- **Tipo**: Banco de dados em memória com suporte a vetores.
- **Vantagens**:
  - Baixa latência.
  - Integração com estruturas de dados Redis (hashes, sorted sets).
- **Exemplo**:
  ```python
  from redis.commands.search.field import VectorField
  # Configuração do índice vetorial em Redis
  ```

---

## Critérios de escolha
| Critério          | FAISS | Chroma | Pinecone | Weaviate | Milvus | Qdrant | Redis |
|-------------------|-------|--------|----------|----------|--------|--------|-------|
| **Performance**   | Alta  | Média  | Alta     | Alta     | Alta   | Alta   | Alta  |
| **Escalabilidade**| Baixa | Média  | Alta     | Alta     | Alta   | Alta   | Média