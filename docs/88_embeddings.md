```markdown
# **Embeddings: Transformar Texto em Vetores**

## **1. Introdução**
Embeddings são representações vetoriais de texto que capturam significado semântico em um espaço dimensional contínuo. São fundamentais em **RAG (Retrieval-Augmented Generation)** para indexar, buscar e recuperar informações relevantes com base em similaridade vetorial.

---

## **2. Conceitos Básicos**

### **2.1 O que são Embeddings?**
- **Definição**: Vetores numéricos que mapeiam texto (palavras, sentenças, documentos) para um espaço onde similaridade semântica é preservada.
- **Dimensão**: Tipicamente 768, 1024 ou 3072 dimensões (depende do modelo).
- **Exemplo**:
  - `"Cachorro"` → `[0.2, -0.1, 0.5, ..., 0.3]` (vetor de 768 dimensões).
  - `"Gato"` → `[0.1, -0.2, 0.6, ..., 0.4]` (mais próximo de `"Cachorro"` do que `"Carro"`).

### **2.2 Por que usar Embeddings?**
- **Busca Semântica**: Recupera documentos relevantes mesmo com termos diferentes (ex: `"como consertar um pneu"` vs. `"troca de roda"`).
- **Redução de Dimensionalidade**: Converte texto bruto em representações compactas e computáveis.
- **Integração com ML**: Modelos como **FAISS**, **Annoy** ou **Pinecone** usam embeddings para busca eficiente.

---

## **3. Modelos de Embeddings Populares**

| Modelo               | Tipo          | Dimensões | Uso Típico                     |
|----------------------|---------------|-----------|--------------------------------|
| `text-embedding-ada-002` (OpenAI) | Texto         | 1536      | Busca semântica, RAG           |
| `all-MiniLM-L6-v2`   | Sentença      | 384       | Similaridade de frases         |
| `sentence-transformers/multi-qa-mpnet-base-dot-v1` | Multilíngue  | 768       | Busca em múltiplos idiomas     |
| `BAAI/bge-small-en`  | Texto         | 384       | Eficiência em baixa dimensão   |

---

## **4. Implementação Prática com LangChain**

### **4.1 Instalação**
```bash
pip install langchain sentence-transformers faiss-cpu  # ou faiss-gpu
```

### **4.2 Carregar um Modelo de Embeddings**
```python
from langchain_community.embeddings import HuggingFaceEmbeddings

# Modelo local (ex: 'all-MiniLM-L6-v2')
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Modelo via API (ex: OpenAI)
# from langchain_openai import OpenAIEmbeddings
# embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
```

### **4.3 Gerar Embeddings para um Texto**
```python
texto = "Como funciona um motor a combustão?"
embedding = embeddings.embed_query(texto)  # Para consultas
print(f"Dimensões: {len(embedding)}")
print(f"Primeiros 5 valores: {embedding[:5]}")
```

### **4.4 Armazenar e Buscar com FAISS**
```python
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# Criar documentos
docs = [
    Document(page_content="Um motor a combustão queima combustível para gerar movimento."),
    Document(page_content="A vela de ignição dispara uma faísca para iniciar a combustão."),
]

# Indexar com embeddings
db = FAISS.from_documents(docs, embeddings)

# Buscar documentos similares
query = "Qual a função da vela de ignição?"
resultados = db.similarity_search(query, k=1)  # Top 1 resultado
print(resultados[0].page_content)
```

---

## **5. Métricas de Similaridade**
LangChain usa **similaridade cosseno** (cosine similarity) por padrão, mas você pode ajustar:

```python
# Similaridade cosseno (padrão)
similaridade = resultados[0].metadata.get("similarity", 0.0