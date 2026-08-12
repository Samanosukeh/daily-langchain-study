```python
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Documentos de exemplo para teste
docs = [
    Document(page_content="O Python é uma linguagem de programação de alto nível."),
    Document(page_content="LangChain é uma biblioteca para desenvolvimento de aplicações com LLMs."),
    Document(page_content="O FAISS é uma biblioteca para busca de similaridade eficiente."),
]

# Carregar embeddings (usando modelo pequeno para teste)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Criar índice vetorial com FAISS
vector_store = FAISS.from_documents(docs, embeddings)

# Função para busca por similaridade
def similarity_search(query: str, k: int = 2) -> list[Document]:
    return vector_store.similarity_search(query, k=k)

# Teste da busca
resultados = similarity_search("Qual biblioteca é usada para busca de similaridade?")
for doc in resultados:
    print(f"Conteúdo: {doc.page_content}\nScore: {doc.metadata.get('score', 'N/A')}\n")
```