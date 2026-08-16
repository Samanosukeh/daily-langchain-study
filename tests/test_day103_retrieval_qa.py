```python
import pytest
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFaceHub
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader

@pytest.fixture
def documents():
    loader = TextLoader("docs/test.txt")
    return loader.load()

@pytest.fixture
def text_splitter():
    return CharacterTextSplitter(chunk_size=100, chunk_overlap=20)

@pytest.fixture
def embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

@pytest.fixture
def vectorstore(documents, text_splitter, embeddings):
    texts = text_splitter.split_documents(documents)
    return FAISS.from_documents(texts, embeddings)

@pytest.fixture
def llm():
    return HuggingFaceHub(
        repo_id="google/flan-t5-large",
        model_kwargs={"temperature": 0.5, "max_length": 512}
    )

@pytest.fixture
def qa_chain(vectorstore, llm):
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

def test_retrieval_qa_answers_based_on_context(qa_chain):
    query = "Qual é a capital do Brasil?"
    expected_answer = "Brasília"

    result = qa_chain.run(query)
    assert expected_answer.lower() in result.lower(), \
        f"Resposta esperada '{expected_answer}' não encontrada no resultado: {result}"

def test_retrieval_qa_handles_unknown_questions(qa_chain):
    query = "Qual é a capital da Lua?"
    result = qa_chain.run(query)

    assert "não sei" in result.lower() or "não tenho informação" in result.lower(), \
        f"Resposta inesperada para pergunta desconhecida: {result}"

def test_retrieval_qa_with_multiple_contexts(qa_chain):
    query = "Quem foi o primeiro presidente do Brasil?"
    expected_answer = "Deodoro da Fonseca"

    result = qa_chain.run(query)
    assert expected_answer.lower() in result.lower(), \
        f"Resposta esperada '{expected_answer}' não encontrada no resultado: {result}"
```