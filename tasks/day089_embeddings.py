```python
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Inicializa o gerador de embeddings com o modelo desejado
model_name = "sentence-transformers/all-mpnet-base-v2"
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs={"device": "cpu"},  # ou "cuda" se disponível
    encode_kwargs={"normalize_embeddings": True}  # normalização opcional
)

# Exemplo de texto para gerar embeddings
textos = [
    "O processamento de linguagem natural é uma área fascinante da IA.",
    "LangChain facilita a integração de modelos de linguagem em aplicações.",
    "Embeddings são representações vetoriais de textos que capturam seu significado."
]

# Gera embeddings para cada texto
embeddings_gerados = embeddings.embed_documents(textos)

# Exibe o formato dos embeddings (vetores de float)
for i, embedding in enumerate(embeddings_gerados):
    print(f"Texto {i+1}:")
    print(f"Embedding (shape: {len(embedding)}) -> {embedding[:5]}... (primeiros 5 valores)")
    print("-" * 50)

# Exemplo de uso em um documento LangChain
documentos = [
    Document(page_content="LangChain é uma framework para desenvolvimento com LLMs."),
    Document(page_content="HuggingFace fornece modelos de linguagem de código aberto.")
]

embeddings_documentos = embeddings.embed_documents([doc.page_content for doc in documentos])

for doc, emb in zip(documentos, embeddings_documentos):
    print(f"Documento: {doc.page_content[:30]}...")
    print(f"Embedding (shape: {len(emb)}) -> {emb[:3]}...")
    print("-" * 50)
```