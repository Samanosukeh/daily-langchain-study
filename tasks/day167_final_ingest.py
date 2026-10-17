```python
import os
from langchain.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFaceHub
from langchain.chains import RetrievalQA

# Configurações
DOCS_DIR = "docs"
CHROMA_PATH = "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
LLM_MODEL = "google/flan-t5-large"
TEMPERATURE = 0.7

def carregar_documentos():
    """Carrega documentos de um diretório."""
    loaders = {
        ".pdf": PyPDFLoader,
        ".txt": TextLoader,
    }

    documentos = []
    for ext, loader_cls in loaders.items():
        loader = DirectoryLoader(
            path=DOCS_DIR,
            glob=f"**/*{ext}",
            loader_cls=loader_cls,
            show_progress=True
        )
        documentos.extend(loader.load())

    return documentos

def dividir_documentos(documentos):
    """Divide documentos em chunks menores."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documentos)
    return chunks

def criar_embeddings(chunks):
    """Cria embeddings dos chunks."""
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"}
    )

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    return db

def inicializar_retriever(db):
    """Inicializa o retriever do vetor store."""
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    return retriever

def inicializar_llm():
    """Inicializa o modelo de linguagem."""
    llm = HuggingFaceHub(
        repo_id=LLM_MODEL,
        model_kwargs={
            "temperature": TEMPERATURE,
            "max_length": 512
        }
    )
    return llm

def criar_cadeia(retriever, llm):
    """Cria a cadeia de QA."""
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

def main():
    # 1. Carregar documentos
    print("Carregando documentos...")
    documentos = carregar_documentos()

    # 2. Dividir documentos em chunks
    print("Dividindo documentos...")
    chunks = dividir_documentos(documentos)

    # 3. Criar embeddings e salvar no vetor store
    print("Criando embeddings...")
    db = criar_embeddings(chunks)
    db.persist()

    # 4. Inicializar retriever
    retriever = inicializar_retriever(db)

    # 5. Inicializar LLM
    llm = inicializar_llm()

    # 6. Criar cadeia de QA
    qa_chain = criar_cadeia(retriever, llm)

    # 7. Testar a cadeia
    print("\nPergunte algo sobre os documentos (ou 'sair' para encerrar):")
    while True:
        pergunta = input("> ")
        if pergunta.lower() == "sair":
            break

        resposta = qa_chain({"query": pergunta})
        print("\nResposta:", resposta["result"])
        print("Documentos usados:", resposta["source_documents"])
        print("-" * 50)

if __name__ == "__main__":
    main()
```