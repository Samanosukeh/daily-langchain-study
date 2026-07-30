```markdown
# **Embeddings: Transformar Texto em Vetores Numéricos**

| **Aspecto**          | **Word2Vec (CBOW/Skip-gram)** | **GloVe** | **FastText** | **BERT (Sentence Embeddings)** | **Sentence-BERT (SBERT)** |
|----------------------|-------------------------------|-----------|--------------|-------------------------------|---------------------------|
| **Base Teórica**     | Redes neurais simples         | Estatística (co-ocorrência) | N-gramas + subword | Transformers (autoencoder) | Transformers + fine-tuning |
| **Representação**    | Vetores por palavra           | Vetores por palavra | Vetores por palavra + subword | Vetores por palavra/sentença | Vetores por sentença |
| **Contexto**         | Limitado à palavra vizinha    | Co-ocorrência global | Subwords + contexto local | Bidirecional (todo texto) | Otimizado para similaridade semântica |
| **Dimensionalidade** | Fixa (ex: 300d)               | Fixa (ex: 300d) | Fixa (ex: 300d) | Variável (ex: 768d) | Variável (ex: 384d/768d) |
| **Treino**           | Supervisionado (corpus)       | Não supervisionado (corpus) | Não supervisionado (corpus) | Auto-supervisionado (corpus) | Fine-tuning em pares de sentenças |
| **Subword Support**  | ❌ Não                        | ❌ Não    | ✅ Sim       | ❌ Não (mas tokens subword) | ❌ Não (mas tokens subword) |
| **Similaridade**     | Cosine entre palavras         | Cosine entre palavras | Cosine entre palavras | Pooling + atenção (sentença) | Pooling + fine-tuning (alta precisão) |
| **Uso em LangChain** | Embeddings básicos (ex: `text-embedding-ada-002`) | Raro | Embeddings robustos para OOV | Embeddings contextualizados | Melhor para RAG, busca semântica |
| **Performance**      | Baixa (contexto limitado)     | Média     | Alta (OOV)   | Alta (contexto global) | Muito alta (otimizado para similaridade) |
| **Exemplo de Uso**   | `gensim.models.Word2Vec`      | `glove-python` | `fasttext` | `sentence-transformers/all-MiniLM-L6-v2` | `all-mpnet-base-v2` |

---

### **Quando Usar Cada Um?**
- **Word2Vec/GloVe/FastText**: Embeddings rápidos para palavras isoladas (ex: dicionários, vocabulário controlado).
- **BERT/SBERT**: Embeddings contextualizados para frases/sentenças (ex: busca semântica, RAG, clustering).
- **FastText**: Ideal para línguas com morfologia rica (ex: português, alemão) ou OOV (Out-of-Vocabulary).
- **SBERT**: Melhor para tarefas de similaridade (ex: sistemas de recomendação, agrupamento de documentos).

---
### **LangChain + Embeddings**
```python
# Exemplo com LangChain (usando Sentence-BERT)
from langchain.embeddings import HuggingFaceEmbeddings

model_name = "sentence-transformers/all-mpnet-base-v2"
embeddings = HuggingFaceEmbeddings(model_name=model_name)

text = "O LangChain facilita a integração de LLMs com embeddings."
embedding = embeddings.embed_query(text)  # Vetor numérico (384d)
```
```python
# Comparação de similaridade com FastText (para OOV)
from langchain_community.embeddings import FastTextEmbeddings

ft_embeddings = FastTextEmbeddings(model_name="cc.pt.300.bin")  # Modelo pré-treinado em português
```
```python
# Embeddings com OpenAI (para casos simples)
from langchain_openai import OpenAIEmbeddings

openai_embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
```
```