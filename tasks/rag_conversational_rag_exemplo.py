```python
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Configuração mínima
llm = ChatOpenAI(model="gpt-3.5-turbo")
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# Base de conhecimento (exemplo com 3 trechos)
docs = [
    "O Python é uma linguagem de programação de alto nível.",
    "LangChain é um framework para aplicações com LLMs.",
    "RAG combina recuperação de informações com geração de texto."
]

# Indexação vetorial
vectorstore = FAISS.from_texts(docs, embeddings)
retriever = vectorstore.as_retriever()

# Template de prompt minimalista
template = """Responda apenas com base no contexto fornecido:
Contexto: {context}
Pergunta: {question}
Resposta:"""
prompt = ChatPromptTemplate.from_template(template)

# Pipeline RAG
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)

# Execução
resposta = chain.invoke("O que é RAG?")
print(resposta.content)
```