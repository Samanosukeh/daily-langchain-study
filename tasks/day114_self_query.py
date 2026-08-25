```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

# Documentos fictícios (substitua pela sua base de dados real)
documents = [
    {"page_content": "O Python é uma linguagem de programação de alto nível.", "metadata": {"source": "docs/python.md", "year": 2020}},
    {"page_content": "LangChain é uma biblioteca para aplicações de linguagem.", "metadata": {"source": "docs/langchain.md", "year": 2023}},
    {"page_content": "O framework Django é usado para desenvolvimento web.", "metadata": {"source": "docs/django.md", "year": 2018}},
    {"page_content": "Machine Learning envolve treinamento de modelos com dados.", "metadata": {"source": "docs/ml.md", "year": 2022}},
]

# Template para extração de filtro pelo LLM
prompt = ChatPromptTemplate.from_messages([
    ("system", """
    Você extrai filtros relevantes dos metadados dos documentos com base na query do usuário.
    Retorne apenas o filtro em formato JSON válido. Exemplo de saída:
    {{"year": {{"$gte": 2020}}}}

    Query do usuário: {query}
    """),
    ("human", "{query}"),
])

# Modelo de linguagem
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Extração do filtro
extractor = prompt | llm | StrOutputParser()

# Função para aplicar o filtro aos documentos
def apply_filter(documents, filter_str):
    import json
    filter_dict = json.loads(filter_str)

    filtered_docs = []
    for doc in documents:
        match = True
        for key, condition in filter_dict.items():
            if key not in doc["metadata"]:
                match = False
                break
            for op, value in condition.items():
                if op == "$gte" and not (doc["metadata"][key] >= value):
                    match = False
                    break
                elif op == "$lte" and not (doc["metadata"][key] <= value):
                    match = False
                    break
                elif op == "$eq" and not (doc["metadata"][key] == value):
                    match = False
                    break
        if match:
            filtered_docs.append(doc)
    return filtered_docs

# Pipeline completo
query = "Mostre artigos sobre Python ou Machine Learning publicados após 2020"

filter_str = extractor.invoke({"query": query})
filtered_docs = apply_filter(documents, filter_str)

print("Filtro gerado pelo LLM:", filter_str)
print("\nDocumentos filtrados:")
for doc in filtered_docs:
    print(f"- {doc['page_content']} (Ano: {doc['metadata']['year']})")
```