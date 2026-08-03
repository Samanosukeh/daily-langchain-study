```python
# tasks/day092_faiss_vector_store.py
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# 1. Dados de exemplo (substitua pela sua fonte real)
textos = [
    "O LangChain é uma biblioteca para desenvolvimento de aplicações com LLMs.",
    "FAISS é uma biblioteca para busca eficiente de vetores em alta dimensão.",
    "RAG combina recuperação de informações com geração de linguagem.",
    "O HuggingFace Embeddings converte texto em vetores numéricos."
]

# 2. Divisão dos textos em chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=10
)
docs = [Document(page_content=texto) for texto in textos]
splits = text_splitter.split_documents(docs)

# 3. Embeddings (usando modelo pré-treinado)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

# 4. Criação do Vector Store local com FAISS
vector_store = FAISS.from_documents(
    documents=splits,
    embedding=embeddings
)

# 5. Salvando o vector store para uso futuro
vector_store.save_local("faiss_index")

# 6. Carregando o vector store salvo (opcional)
loaded_vector_store = FAISS.load_local(
    "faiss_index",
    embeddings=embeddings,
    allow_dangerous_deserialization=True  # Necessário para versões recentes
)

# 7. Exemplo de busca semântica
query = "O que é RAG?"
docs_relevantes = loaded_vector_store.similarity_search(query, k=2)
print(f"Documentos relevantes para '{query}':")
for doc in docs_relevantes:
    print(f"- {doc.page_content}")
```