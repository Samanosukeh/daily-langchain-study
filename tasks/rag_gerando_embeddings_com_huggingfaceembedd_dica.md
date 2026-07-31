```markdown
# Dicas Rápidas: Gerando Embeddings com HuggingFace

1. **Instale as dependências necessárias**:
   ```bash
   pip install transformers torch sentence-transformers
   ```

2. **Carregue um modelo de embedding**:
   ```python
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('all-MiniLM-L6-v2')  # Modelo leve e eficiente
   ```

3. **Gere embeddings para um texto**:
   ```python
   embeddings = model.encode("Este é um exemplo de texto.")
   print(embeddings.shape)  # (384,) para o modelo 'all-MiniLM-L6-v2'
   ```

4. **Embeddings para múltiplos textos**:
   ```python
   texts = ["Texto 1", "Texto 2", "Texto 3"]
   embeddings = model.encode(texts)
   print(embeddings.shape)  # (3, 384)
   ```

5. **Salve embeddings em disco**:
   ```python
   import numpy as np
   np.save("embeddings.npy", embeddings)
   ```

6. **Carregue embeddings salvos**:
   ```python
   embeddings = np.load("embeddings.npy")
   ```

7. **Use GPU (se disponível)**:
   ```python
   model = model.to('cuda')
   ```

8. **Ajuste o batch_size para performance**:
   ```python
   embeddings = model.encode(texts, batch_size=32)
   ```

9. **Normalize embeddings (opcional)**:
   ```python
   embeddings = model.encode(texts, normalize_embeddings=True)
   ```

10. **Compare embeddings com cosseno**:
    ```python
    from sklearn.metrics.pairwise import cosine_similarity
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
    ```

11. **Use modelos maiores para melhor qualidade**:
    ```python
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    ```

12. **Cache de modelos**:
    ```python
    model.save('modelo_cache')
    model = SentenceTransformer('modelo_cache')
    ```

13. **Embeddings para busca semântica**:
    ```python
    query = "Busca por exemplo"
    query_embedding = model.encode(query)
    ```

14. **Armazenamento eficiente com FAISS**:
    ```python
    import faiss
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    ```

15. **Atualize para versões recentes**:
    ```bash
    pip install --upgrade transformers sentence-transformers
    ```
```