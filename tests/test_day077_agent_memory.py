```python
import pytest
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_models import ChatOpenAI
from langchain_core.memory import ChatMessageHistory
from langchain_core.runnables import RunnableConfig

# Mock para simular a store de histórico de mensagens
class MockMessageStore:
    def __init__(self):
        self.store = {}

    def get_session_history(self, session_id: str) -> ChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

@pytest.fixture
def mock_store():
    return MockMessageStore()

@pytest.fixture
def agent_with_memory(mock_store):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente útil."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    llm = ChatOpenAI(model="gpt-4", temperature=0)
    chain = prompt | llm

    agent = RunnableWithMessageHistory(
        chain,
        lambda session_id: mock_store.get_session_history(session_id),
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    return agent, mock_store

def test_agent_lembra_contexto_anterior(agent_with_memory):
    agent, store = agent_with_memory

    # Primeira interação
    config = RunnableConfig(configurable={"session_id": "user1"})
    response1 = agent.invoke({"input": "Qual é o meu nome?"}, config=config)
    assert "nome" in response1.content.lower()

    # Segunda interação com contexto
    response2 = agent.invoke({"input": "E meu sobrenome?"}, config=config)
    assert "sobrenome" in response2.content.lower()

    # Verifica histórico armazenado
    history = store.get_session_history("user1")
    assert len(history.messages) == 4  # 2 do usuário, 2 do assistente
    assert isinstance(history.messages[0], HumanMessage)
    assert isinstance(history.messages[1], AIMessage)

def test_agent_limpa_contexto_por_sessao(agent_with_memory):
    agent, store = agent_with_memory

    # Interação na sessão 1
    config1 = RunnableConfig(configurable={"session_id": "user1"})
    agent.invoke({"input": "Teste sessão 1"}, config=config1)

    # Interação na sessão 2
    config2 = RunnableConfig(configurable={"session_id": "user2"})
    agent.invoke({"input": "Teste sessão 2"}, config=config2)

    # Verifica que as sessões são independentes
    history1 = store.get_session_history("user1")
    history2 = store.get_session_history("user2")
    assert len(history1.messages) == 2
    assert len(history2.messages) == 2
    assert history1.messages[0].content == "Teste sessão 1"
    assert history2.messages[0].content == "Teste sessão 2"

def test_agent_sem_contexto_inicial(agent_with_memory):
    agent, store = agent_with_memory

    config = RunnableConfig(configurable={"session_id": "user3"})
    response = agent.invoke({"input": "O que você sabe sobre mim?"}, config=config)

    # Deve responder que não sabe nada
    assert "não sei" in response.content.lower() or "nenhum" in response.content.lower()
    assert len(store.get_session_history("user3").messages) == 2
```