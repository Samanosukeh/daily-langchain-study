```python
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import PromptTemplate

# Configuração do embeddings (exemplo com HuggingFace)
embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

# Carregar vector store (FAISS)
vector_store = FAISS.load_local(
    "caminho/para/seu/vector_store",
    embeddings,
    allow_dangerous_deserialization=True
)

# Configurar LLM (exemplo com HuggingFace Hub)
llm = HuggingFaceHub(
    repo_id="google/flan-t5-large",
    model_kwargs={"temperature": 0.5, "max_length": 512}
)

# Template de prompt personalizado
template = """Use as seguintes peças de contexto para responder à pergunta no final.
Se você não souber a resposta, diga que não sabe, não tente inventar.

Contexto: {context}
Pergunta: {question}
Resposta útil:"""
prompt = PromptTemplate.from_template(template)

# Criar RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(),
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True
)

# Executar pergunta com contexto
pergunta = "Como funciona o RetrievalQA chain no LangChain?"
resultado = qa_chain({"query": pergunta})

print("Resposta:", resultado["result"])
print("\nDocumentos fonte:")
for doc in resultado["source_documents"]:
    print(f"- {doc.page_content[:100]}...")
```