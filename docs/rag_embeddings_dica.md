```markdown
# Embeddings: transformar texto em vetores numéricos

## O que são embeddings?
- Representações vetoriais densas de texto (palavras, frases, documentos).
- Capturam semântica e contexto (similaridade semântica).
- Usados em RAG, busca vetorial, classificação, clusterização.

## Principais bibliotecas
```python
from sentence_transformers import SentenceTransformer
from transformers import AutoModel
import numpy as np
```

## Modelos populares
- **Sentence-BERT (SBERT)**: `all-MiniLM-L6-v2` (leve, bom para frases).
- **HuggingFace**: `sentence-transformers/all-mpnet-base-v2` (alta qualidade).
- **OpenAI**: `text-embedding-ada-002` (API externa).

## Como gerar embeddings
```python
model = SentenceTransformer('all-MiniLM-L6-v2')
textos = ["Olá mundo", "Python é legal"]
embeddings = model.encode(textos)  # shape: (n_textos, dim_embedding=384)
```

## Normalização e similaridade
```python
embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
similaridade = np.dot(embedding1, embedding2.T)  # Cosseno (0-1)
```

## Armazenamento eficiente
- **FAISS** (Facebook): Indexação vetorial para busca rápida.
- **ChromaDB/Pinecone**: BD vetorial para aplicações em produção.

## Dicas práticas
1. **Pré-processamento**: Remova stopwords se o modelo for sensível.
2. **Batch size**: Processo em lotes (`batch_size=32`) para performance.
3. **Cache**: Armazene embeddings para evitar reprocessamento.
4. **Dimensionalidade**: Reduza com PCA se necessário (`sklearn.decomposition.PCA`).
5. **Avalie**: Teste embeddings em tarefas específicas (ex: busca semântica).

## Exemplo completo
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
query = "Qual a capital da França?"
embedding_query = model.encode(query)
docs = ["Paris é a capital.", "A França fica na Europa."]
embeddings_docs = model.encode(docs)
similaridades = np.dot(embedding_query, embeddings_docs.T)
print(np.argmax(similaridades))  # Índice do documento mais relevante
```
```