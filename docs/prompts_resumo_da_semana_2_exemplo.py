```python
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

# Carregar URLs da semana 2
urls = [
    "https://exemplo.com/semana-2-aula-1",
    "https://exemplo.com/semana-2-aula-2"
]
loader = WebBaseLoader(urls)
docs = loader.load()

# Dividir documentos em chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# Template para sumarização
template = """
Resuma o conteúdo abaixo em 3 pontos principais:

Conteúdo: {text}

Resumo:
"""
prompt = ChatPromptTemplate.from_template(template)

# Modelo de linguagem
model = ChatOpenAI(temperature=0.3)

# Pipeline de sumarização
summarize_chain = {"text": RunnablePassthrough()} | prompt | model

# Processar cada chunk e gerar resumo
for chunk in chunks[:3]:  # Processa apenas 3 chunks para exemplo
    summary = summarize_chain.invoke(chunk.page_content)
    print(f"Resumo do chunk: {summary.content}\n")
```