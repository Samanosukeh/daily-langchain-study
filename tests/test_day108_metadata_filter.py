```python
import pytest
from unittest.mock import MagicMock
from langchain_core.documents import Document
from seu_modulo_rag import FiltroMetadata

@pytest.fixture
def mock_docs():
    return [
        Document(page_content="doc1", metadata={"tipo": "correto"}),
        Document(page_content="doc2", metadata={"tipo": "incorreto"}),
        Document(page_content="doc3", metadata={"tipo": "correto"}),
        Document(page_content="doc4", metadata={"outro": "valor"}),
    ]

def test_filtro_metadata_retorna_apenas_docs_corretos(mock_docs):
    filtro = FiltroMetadata(metadata_chave="tipo", valor_esperado="correto")
    resultado = filtro.filtrar(mock_docs)

    assert len(resultado) == 2
    assert all(doc.metadata.get("tipo") == "correto" for doc in resultado)
    assert all("incorreto" not in doc.metadata.values() for doc in resultado)

def test_filtro_metadata_com_chave_nao_existente(mock_docs):
    filtro = FiltroMetadata(metadata_chave="nao_existe", valor_esperado="correto")
    resultado = filtro.filtrar(mock_docs)

    assert len(resultado) == 0

def test_filtro_metadata_com_valor_diferente(mock_docs):
    filtro = FiltroMetadata(metadata_chave="tipo", valor_esperado="outro_valor")
    resultado = filtro.filtrar(mock_docs)

    assert len(resultado) == 0

def test_filtro_metadata_com_lista_de_valores(mock_docs):
    filtro = FiltroMetadata(metadata_chave="tipo", valor_esperado=["correto", "outro_valor"])
    resultado = filtro.filtrar(mock_docs)

    assert len(resultado) == 2
    assert all(
        doc.metadata.get("tipo") in ["correto", "outro_valor"]
        for doc in resultado
    )

def test_filtro_metadata_com_doc_sem_metadata(mock_docs):
    mock_docs.append(Document(page_content="doc5"))
    filtro = FiltroMetadata(metadata_chave="tipo", valor_esperado="correto")
    resultado = filtro.filtrar(mock_docs)

    assert len(resultado) == 2  # Não inclui o doc5
    assert "doc5" not in [doc.page_content for doc in resultado]
```