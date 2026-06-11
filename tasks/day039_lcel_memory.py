```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_models import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import SystemMessage
from typing import Optional

# Configuração inicial
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Definição do prompt com placeholder para histórico
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="Você é um assistente útil."),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}"),
])

# Função para obter histórico de mensagens por sessão
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Criação do chain com histórico
chain = prompt | llm

# Encapsulando com RunnableWithMessageHistory
with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# Execução com histórico
config = {"configurable": {"session_id": "user123"}}

response = with_message_history.invoke(
    {"input": "Olá, como você está?"},
    config=config,
)
print("Resposta:", response.content)

# Continuando a conversa
response = with_message_history.invoke(
    {"input": "Qual é o meu nome?"},
    config=config,
)
print("Resposta:", response.content)
```