```markdown
# Comparação: RetrievalQA Chain vs. Alternativas Básicas

## **RetrievalQA Chain (LangChain)**
```python
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Setup
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.from_documents(documents, embeddings)
retriever = db.as_retriever(search_kwargs={"k": 3})

# Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# Execução
result = qa_chain({"query": "Qual a capital do Brasil?"})
print(result["result"])  # Resposta + contexto
```

✅ **Vantagens**:
- Integra recuperação + geração em uma única cadeia.
- Suporte a `return_source_documents` para rastreabilidade.
- Configurável (`chain_type="map_reduce"`, `"refine"`, etc.).
- Ideal para RAG (Retrieval-Augmented Generation).

❌ **Desvantagens**:
- Overhead para queries simples (sem necessidade de recuperação).
- Requer setup de embeddings e vector store.

---

## **Alternativa: LLM + Prompt Simples**
```python
from langchain.prompts import PromptTemplate

template = """Responda apenas com base no contexto abaixo:
Contexto: {context}
Pergunta: {question}
Resposta:"""

prompt = PromptTemplate.from_template(template)
chain = prompt | llm

result = chain.invoke({
    "context": "A capital do Brasil é Brasília.",
    "question": "Qual a capital do Brasil?"
})
print(result.content)
```

✅ **Vantagens**:
- Simplicidade extrema (sem dependências de vector stores).
- Baixo custo computacional para contexto estático.

❌ **Desvantagens**:
- Sem recuperação dinâmica (contexto deve ser injetado manualmente).
- Limitado a perguntas pré-definidas no prompt.

---
## **Alternativa: StuffDocumentsChain**
```python
from langchain.chains import StuffDocumentsChain, LLMChain
from langchain.docstore.document import Document

# Chain de síntese
llm_chain = LLMChain(llm=llm, prompt=prompt)
stuff_chain = StuffDocumentsChain(
    llm_chain=llm_chain,
    document_variable_name="context"
)

# Execução
docs = [Document(page_content="Brasília é a capital do Brasil.")]
result = stuff_chain.run(input_documents=docs, question="Qual a capital?")
```

✅ **Vantagens**:
- Útil quando o contexto já está em formato de documentos.
- Menos acoplado a vector stores.

❌ **Desvantagens**:
- Não lida com recuperação automática.
- Requer formatação prévia dos documentos.

---
## **Quando Usar Cada Uma?**
| **Caso**                     | **RetrievalQA** | **Prompt Simples** | **StuffDocumentsChain** |
|------------------------------|----------------|--------------------|-------------------------|
| Base de conhecimento dinâmica | ✅ Sim         | ❌ Não             | ❌ Não                  |
| Contexto estático            | ⚠️ Overkill    | ✅ Ideal           | ✅ Ideal                |
| Rastreabilidade de fontes    | ✅ Sim         | ❌ Não             | ❌ Não                  |
| Baixo custo de setup         | ❌ Não         | ✅ Sim             | ✅ Sim                  |
```