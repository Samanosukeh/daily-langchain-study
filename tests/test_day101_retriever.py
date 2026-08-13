```python
import pytest
from typing import List
from unittest.mock import MagicMock, patch
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

@pytest.fixture
def mock_embeddings():
    return MagicMock(spec=Embeddings)

@pytest.fixture
def mock_faiss_index():
    return MagicMock(spec=FAISS)

@pytest.fixture
def retriever(mock_faiss_index):
    from src.retriever import Retriever
    return Retriever(vector_store=mock_faiss_index)

def test_retriever_returns_k_documents(retriever, mock_faiss_index):
    # Configura mock para retornar documentos
    k = 3
    mock_documents = [
        Document(page_content=f"Documento {i}", metadata={"id": i})
        for i in range(k)
    ]
    mock_faiss_index.similarity_search.return_value = mock_documents

    # Executa
    result = retriever.retrieve(query="teste", k=k)

    # Verifica
    assert len(result) == k
    assert all(isinstance(doc, Document) for doc in result)
    mock_faiss_index.similarity_search.assert_called_once_with(
        query="teste", k=k
    )

def test_retriever_returns_empty_list_when_no_documents(mock_faiss_index):
    # Configura mock para retornar lista vazia
    k = 2
    mock_faiss_index.similarity_search.return_value = []
    retriever = Retriever(vector_store=mock_faiss_index)

    # Executa
    result = retriever.retrieve(query="inexistente", k=k)

    # Verifica
    assert result == []
    assert len(result) == 0

@pytest.mark.parametrize("k", [1, 5, 10])
def test_retriever_returns_exactly_k_documents(retriever, mock_faiss_index, k):
    # Configura mock para retornar k documentos
    mock_documents = [
        Document(page_content=f"Documento {i}", metadata={"id": i})
        for i in range(k)
    ]
    mock_faiss_index.similarity_search.return_value = mock_documents

    # Executa
    result = retriever.retrieve(query="teste", k=k)

    # Verifica
    assert len(result) == k
    assert all(isinstance(doc, Document) for doc in result)

def test_retriever_passes_correct_parameters_to_vector_store(retriever, mock_faiss_index):
    # Executa
    query = "consulta avançada"
    k = 4
    retriever.retrieve(query=query, k=k)

    # Verifica
    mock_faiss_index.similarity_search.assert_called_once_with(
        query=query, k=k
    )

def test_retriever_handles_different_document_types(retriever, mock_faiss_index):
    # Configura mock para retornar documentos com diferentes metadados
    mock_documents = [
        Document(page_content="Texto 1", metadata={"source": "artigo"}),
        Document(page_content="Texto 2", metadata={"source": "livro", "página": 42}),
        Document(page_content="Texto 3", metadata={"url": "http://exemplo.com"}),
    ]
    mock_faiss_index.similarity_search.return_value = mock_documents

    # Executa
    result = retriever.retrieve(query="teste", k=3)

    # Verifica
    assert len(result) == 3
    assert all(isinstance(doc, Document) for doc in result)
```