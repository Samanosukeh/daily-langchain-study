```python
import pytest
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

@pytest.fixture
def sample_documents():
    return [
        Document(page_content="O Python é uma linguagem de programação de alto nível."),
        Document(page_content="O FAISS é uma biblioteca para busca de similaridade eficiente."),
        Document(page_content="LangChain é um framework para aplicações com LLMs."),
        Document(page_content="Pytest é uma ferramenta para testes em Python."),
    ]

@pytest.fixture
def faiss_index(sample_documents):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return FAISS.from_documents(sample_documents, embeddings)

def test_faiss_recupera_documento_mais_similar(faiss_index, sample_documents):
    query = "ferramenta para testes"
    docs = faiss_index.similarity_search(query, k=1)
    assert len(docs) == 1
    assert "Pytest" in docs[0].page_content

def test_faiss_recupera_documentos_similares_ordenados(faiss_index):
    query = "linguagem de programação"
    docs = faiss_index.similarity_search(query, k=2)
    assert len(docs) == 2
    assert "Python" in docs[0].page_content
    assert "LangChain" in docs[1].page_content

def test_faiss_score_similaridade(faiss_index):
    query = "biblioteca para busca eficiente"
    docs_and_scores = faiss_index.similarity_search_with_score(query, k=1)
    assert len(docs_and_scores) == 1
    assert docs_and_scores[0][1] < 0.5  # Score de similaridade baixo (mais similar)
```