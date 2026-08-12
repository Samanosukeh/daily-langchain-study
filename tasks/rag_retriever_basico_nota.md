```markdown
# Notas Técnicas: Configuração Avançada de Retrievers em LangChain

## 1. Personalização de Embeddings para Domínios Específicos

Ao trabalhar com retrievers em domínios técnicos (ex: jurídico, médico), a qualidade dos embeddings impacta diretamente a relevância dos resultados. A biblioteca permite substituir o modelo padrão de embeddings:

```python
from langchain_community.embeddings import HuggingFaceEmbeddings

# Configuração para embeddings multilingues (ex: BERT-base-multilingual)
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={'device': 'cpu'},  # Ou 'cuda' para GPU
    encode_kwargs={'normalize_embeddings': True}  # Normalização para métricas de similaridade
)
```

**Observações:**
- Modelos menores (ex: `all-MiniLM-L6-v2`) são ideais para ambientes com restrição de recursos.
- Para domínios específicos, considere fine-tuning com dados próprios.

---

## 2. Otimização de Performance com Chunking Estratégico

O tamanho dos chunks afeta a precisão do retriever. Para textos técnicos:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,       # Tamanho ideal para modelos como BERT
    chunk_overlap=128,    # Overlap para manter contexto
    separators=["\n\n", "\n", " ", ""]  # Prioriza quebras de seção
)
```

**Recomendações:**
- Para código fonte: use `Language` do `tree-sitter` como separador.
- Evite chunks menores que 100 tokens em domínios técnicos.

---
## 3. Persistência de Vetores com FAISS

Armazenar embeddings localmente acelera buscas subsequentes:

```python
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

# Carregar documentos (ex: após processamento)
docs = [Document(page_content=texto, metadata={"source": "manual.pdf"})]

# Criar/indexar vetores
db = FAISS.from_documents(docs, embedding_model)
db.save_local("vetores_tecnicos")  # Persiste em disco

# Carregar posteriormente
db = FAISS.load_local("vetores_tecnicos", embedding_model, allow_dangerous_deserialization=True)
```

**Cuidados:**
- O arquivo `index.faiss` + `index.pkl` deve ser versionado junto ao código.
- Para grandes volumes (>100k chunks), considere `Chroma` ou `Weaviate`.

---
## 4. Filtragem por Metadata em Retrievers Híbridos

Combinação de busca vetorial + filtros de metadata:

```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever

# BM25 para busca lexical
bm25_retriever = BM25Retriever.from_documents(docs)
bm25_retriever.k = 10

# Filtro por metadata (ex: apenas seções "API")
metadata_filter = {"source": "manual.pdf", "section": "API Reference"}

# Ensemble (BM25 + Vetorial)
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, db.as_retriever()],
    weights=[0.3, 0.7]  # Peso para cada retriever
)
```

**Casos de uso:**
- Buscas em documentação multi-produto.
- Filtros por data, autor ou tags específicas.

---
## Referências
- [LangChain Retrievers](https://python.langchain.com/docs/modules/data_connection/retrievers/)
- [FAISS Indexing](https://github.com/facebookresearch/faiss)
- [HuggingFace Embeddings](https://huggingface.co/sentence-transformers)
```