```markdown
# Comentários no Pipeline RAG Completo

## Visão Geral
Este documento descreve os comentários críticos inseridos no pipeline RAG (Retrieval-Augmented Generation) completo, com foco em cada etapa do processo.

---

## 1. Carregamento de Documentos (`DocumentLoader`)
```python
# Carrega documentos da pasta especificada
# @param source_dir: Caminho para a pasta contendo os documentos
# @return: Lista de documentos carregados
documents = loader.load_directory(source_dir)
```

**Comentário:**
- `source_dir` deve ser validado para evitar erros de caminho.
- Considerar suporte a múltiplos formatos (PDF, TXT, DOCX).

---

## 2. Divisão de Textos (`TextSplitter`)
```python
# Divide documentos em chunks de tamanho 1000 com sobreposição de 200
# @param chunk_size: Tamanho de cada chunk (padrão: 1000)
# @param chunk_overlap: Sobreposição entre chunks (padrão: 200)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = splitter.split_documents(documents)
```

**Comentário:**
- Ajustar `chunk_size` e `chunk_overlap` conforme o modelo de embedding.
- Evitar chunks muito pequenos para não perder contexto.

---

## 3. Embeddings (`Embeddings`)
```python
# Gera embeddings para os chunks usando modelo 'all-MiniLM-L6-v2'
# @param model_name: Nome do modelo de embedding (padrão: 'all-MiniLM-L6-v2')
embeddings = HuggingFaceEmbeddings(model_name=model_name)
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings
)
```

**Comentário:**
- Verificar compatibilidade do modelo com o tamanho dos chunks.
- Considerar persistência do `vectorstore` para reutilização.

---

## 4. Recuperação (`Retriever`)
```python
# Configura o retriever para buscar os 4 chunks mais relevantes
# @param k: Número de chunks a serem recuperados (padrão: 4)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
```

**Comentário:**
- Ajustar `k` conforme a necessidade de contexto.
- Validar se os chunks recuperados são realmente relevantes.

---
## 5. Prompt Template (`PromptTemplate`)
```python
# Define o template de prompt para geração de resposta
# @param context: Chunks recuperados
# @param question: Pergunta do usuário
prompt_template = """
Responda à pergunta com base no contexto fornecido.
Contexto: {context}
Pergunta: {question}
Resposta:
"""
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template
)
```

**Comentário:**
- Personalizar o template para melhorar a qualidade das respostas.
- Incluir instruções claras para o modelo.

---
## 6. Geração (`LLMChain`)
```python
# Inicializa o modelo de linguagem (ex: 'llama2')
# @param model_name: Nome do modelo (padrão: 'llama2')
llm = HuggingFaceHub(
    repo_id=model_name,
    model_kwargs={"temperature": 0.5, "max_length": 1024}
)
chain = LLMChain(llm=llm, prompt=prompt)
```

**Comentário:**
- Ajustar `temperature` para controlar a criatividade do modelo.
- Monitorar `max_length` para evitar respostas truncadas.

---
## 7. Pipeline Completo (`RAGPipeline`)
```python
# Executa o pipeline RAG completo
# @param question: Pergunta do usuário
# @return: Resposta gerada
def run_rag_pipeline(question):
    # Recupera chunks relevantes
    docs = retriever.get_relevant_documents(question)

    # Gera resposta usando o LLM
    response = chain.run({
        "context": "\n".join([doc.page_content for doc in docs]),
        "question": question
    })

    return response
```

**Comentário:**
- Validar a entrada `question` para evitar erros.
- Logar os chunks recuperados para debug.
```

---
**Arquivo:** `task_rag_pipeline.py`
**Tópico:** `rag`