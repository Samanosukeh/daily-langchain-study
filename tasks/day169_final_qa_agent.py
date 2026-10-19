```python
# projeto_final/agent.py
from typing import Optional, List, Dict, Any
from langchain.agents import AgentExecutor, initialize_agent
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore
from langchain_core.language_models import BaseLanguageModel
from langchain_core.callbacks import BaseCallbackManager
import os

class QAAgent:
    """
    Agente de Q&A com retrieval para responder perguntas com base em documentos.
    """

    def __init__(
        self,
        model: BaseLanguageModel,
        vectorstore_path: str = "faiss_index",
        embeddings_model_name: str = "sentence-transformers/all-mpnet-base-v2",
        callback_manager: Optional[BaseCallbackManager] = None,
    ):
        self.model = model
        self.vectorstore_path = vectorstore_path
        self.embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        self.callback_manager = callback_manager
        self.vectorstore: Optional[VectorStore] = None
        self.retriever = None
        self.qa_chain = None
        self.agent = None

    def load_documents(self, directory: str) -> List[Any]:
        """Carrega documentos de um diretório."""
        loader = DirectoryLoader(directory, glob="*.txt", loader_cls=TextLoader)
        return loader.load()

    def split_documents(self, documents: List[Any]) -> List[Any]:
        """Divide documentos em chunks."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        return text_splitter.split_documents(documents)

    def create_vectorstore(self, documents: List[Any]) -> VectorStore:
        """Cria um vetor de armazenamento FAISS."""
        return FAISS.from_documents(documents, self.embeddings)

    def save_vectorstore(self, vectorstore: VectorStore) -> None:
        """Salva o vetor de armazenamento em disco."""
        vectorstore.save_local(self.vectorstore_path)

    def load_vectorstore(self) -> Optional[VectorStore]:
        """Carrega o vetor de armazenamento salvo."""
        if os.path.exists(self.vectorstore_path):
            return FAISS.load_local(
                self.vectorstore_path,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
        return None

    def setup_retrieval_qa(self) -> RetrievalQA:
        """Configura a cadeia de Q&A com retrieval."""
        prompt_template = """Use as seguintes peças de contexto para responder à pergunta no final.
Se você não sabe a resposta, apenas diga que não sabe, não tente inventar uma resposta.

Contexto: {context}

Pergunta: {question}

Resposta:"""

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        return RetrievalQA.from_chain_type(
            llm=self.model,
            chain_type="stuff",
            retriever=self.retriever,
            chain_type_kwargs={"prompt": PROMPT},
            callback_manager=self.callback_manager,
        )

    def setup_agent(self) -> AgentExecutor:
        """Configura o agente com a cadeia de Q&A."""
        return initialize_agent(
            agent="zero-shot-react-description",
            tools=[self.qa_chain],
            llm=self.model,
            callback_manager=self.callback_manager,
            verbose=True,
        )

    def initialize(self, docs_directory: str) -> None:
        """Inicializa o agente com documentos."""
        # Carregar ou criar vetor de armazenamento
        self.vectorstore = self.load_vectorstore()
        if not self.vectorstore:
            documents = self.load_documents(docs_directory)
            split_docs = self.split_documents(documents)
            self.vectorstore = self.create_vectorstore(split_docs)
            self.save_vectorstore(self.vectorstore)

        # Configurar retriever
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

        # Configurar cadeia de Q&A
        self.qa_chain = self.setup_retrieval_qa()

        # Configurar agente
        self.agent = self.setup_agent()

    def run(self, question: str) -> Dict[str, Any]: