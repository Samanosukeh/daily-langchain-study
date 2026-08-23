```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import format_document
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from typing import List, Optional, Tuple
import uuid

# Configuração do modelo de linguagem
llm = ChatOllama(model="llama3")

# Configuração do retriever (exemplo com Chroma)
vectorstore = Chroma(
    collection_name="task_documents",
    persist_directory="./chroma_db",
    embedding_function=embedding_function  # Substitua pela sua função de embedding
)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 10}
)

# Template de prompt para conversação com histórico
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente especializado em tarefas. Responda com base no contexto fornecido e no histórico da conversa:\n\nContexto:\n{context}"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

# Função para formatar documentos
def format_docs(docs):
    return "\n\n".join(format_document(doc, "{page_content}") for doc in docs)

# Chain principal
def format_context(question: str, history: List[Tuple[str, str]]) -> str:
    # Recupera documentos relevantes
    retrieved_docs = retriever.invoke(question)
    formatted_context = format_docs(retrieved_docs)
    return formatted_context

chain = (
    {
        "context": lambda x: format_context(x["question"], x["history"]),
        "history": lambda x: x["history"],
        "question": lambda x: x["question"]
    }
    | prompt
    | llm
    | StrOutputParser()
)

# Função para gerenciar histórico de conversa
def get_session_history(session_id: str):
    # Implemente a lógica de armazenamento de histórico aqui
    # Exemplo simples com dicionário em memória
    if not hasattr(get_session_history, "store"):
        get_session_history.store = {}
    if session_id not in get_session_history.store:
        get_session_history.store[session_id] = []
    return get_session_history.store[session_id]

# Chain com histórico
conversational_rag_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
    output_messages_key="answer"
)

# Exemplo de uso
session_id = str(uuid.uuid4())
response = conversational_rag_chain.invoke(
    {"question": "Como posso otimizar esta tarefa?", "history": []},
    config={"configurable": {"session_id": session_id}}
)
print(response)

# Continuando a conversa
response = conversational_rag_chain.invoke(
    {"question": "E quanto ao tempo de execução?", "history": [
        HumanMessage(content="Como posso otimizar esta tarefa?"),
        AIMessage(content=response)
    ]},
    config={"configurable": {"session_id": session_id}}
)
print(response)
```