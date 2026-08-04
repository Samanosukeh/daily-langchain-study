```markdown
# Teste: FAISS encontra documento similar

## Verifique a similaridade de embeddings

```python
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Carregue o índice FAISS
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local("meu_indice_faiss", embeddings)

# Consulta de teste
query = "Qual é a capital do Brasil?"
docs = db.similarity_search(query, k=3)

# Exiba os resultados
for doc in docs:
    print(f"Conteúdo: {doc.page_content[:100]}...")
    print(f"Score: {doc.metadata.get('score', 'N/A')}\n")
```

## Debug rápido

1. **Verifique embeddings**:
   ```python
   print(embeddings.embed_query("teste"))
   print(embeddings.embed_documents(["teste"]))
   ```

2. **Teste busca exata**:
   ```python
   docs = db.similarity_search("capital do Brasil", k=1)
   assert "Brasília" in docs[0].page_content, "Documento não encontrado!"
   ```

3. **Ajuste `k`**:
   - Aumente `k` se poucos resultados forem retornados.
   - Diminua `k` se muitos resultados irrelevantes aparecerem.

## Erros comuns

- **Index vazio?**
  Verifique se o índice foi salvo corretamente:
  ```python
  print(f"Número de documentos: {db.index.ntotal}")
  ```

- **Embeddings inconsistentes?**
  Garanta que o modelo de embedding usado no treinamento e na busca é o mesmo.

- **Metadados ausentes?**
  Adicione metadados ao salvar:
  ```python
  db.save_local("meu_indice_faiss", index_name="meu_índice_com_meta")
  ```
```