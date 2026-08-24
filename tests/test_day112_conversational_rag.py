```python
import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_models import FakeListLLM
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import FakeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.rag.conversational_rag import create_conversational_rag_chain

@pytest.fixture
def mock_vectorstore():
    documents = [Document(page_content="Texto de teste para RAG")]
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    embeddings = FakeEmbeddings(size=1352)
    return FAISS.from_documents(texts, embeddings)

@pytest.fixture
def mock_llm():
    return FakeListLLM(responses=["Resposta do LLM"])

@pytest.fixture
def mock_session_manager():
    return MagicMock()

@pytest.fixture
def conversational_rag_chain(mock_vectorstore, mock_llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente útil."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])
    retriever = mock_vectorstore.as_retriever()
    chain = prompt | mock_llm
    return RunnableWithMessageHistory(
        chain,
        lambda _: mock_session_manager,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

def test_conversational_rag_mantém_historico(
    conversational_rag_chain, mock_session_manager, mock_llm
):
    # Configura histórico inicial
    mock_session_manager.messages = [
        HumanMessage(content="Olá, como você está?"),
        AIMessage(content="Estou bem, obrigado!"),
    ]

    # Executa cadeia com nova entrada
    response = conversational_rag_chain.invoke(
        {"input": "Qual é o meu nome?"},
        config={"configurable": {"session_id": "teste"}},
    )

    # Verifica se histórico foi mantido
    assert len(mock_session_manager.messages) == 3
    assert isinstance(mock_session_manager.messages[-2], HumanMessage)
    assert isinstance(mock_session_manager.messages[-1], AIMessage)
    assert "Qual é o meu nome?" in str(mock_session_manager.messages[-2].content)

def test_conversational_rag_cria_novo_historico_se_nao_existir(
    conversational_rag_chain, mock_session_manager
):
    # Garante que não há histórico prévio
    mock_session_manager.messages = []

    # Executa cadeia
    response = conversational_rag_chain.invoke(
        {"input": "Primeira pergunta"},
        config={"configurable": {"session_id": "novo"}},
    )

    # Verifica criação de novo histórico
    assert len(mock_session_manager.messages) == 2
    assert isinstance(mock_session_manager.messages[0], HumanMessage)
    assert isinstance(mock_session_manager.messages[1], AIMessage)

def test_conversational_rag_processa_multiplas_interacoes(
    conversational_rag_chain, mock_session_manager
):
    # Configura histórico com múltiplas interações
    mock_session_manager.messages = [
        HumanMessage(content="Primeira pergunta"),
        AIMessage(content="Resposta 1"),
        HumanMessage(content="Segunda pergunta"),
        AIMessage(content="Resposta 2"),
    ]

    # Executa cadeia
    response = conversational_rag_chain.invoke(
        {"input": "Terceira pergunta"},
        config={"configurable": {"session_id": "multiplas"}},
    )

    # Verifica manutenção de todo o histórico
    assert len(mock_session_manager.messages) == 6
    assert "Terceira pergunta" in str(mock_session_manager.messages[-2].content)
```