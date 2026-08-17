```python
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class MMRRetriever:
    """
    Implementação do MMR (Maximum Marginal Relevance) para recuperação de documentos.
    Combina relevância com diversidade para evitar resultados redundantes.
    """

    def __init__(self, embeddings_model: str = "sentence-transformers/all-mpnet-base-v2", k: int = 5):
        """
        Inicializa o retriever MMR.

        Args:
            embeddings_model: Modelo de embeddings a ser utilizado
            k: Número de documentos a serem retornados
        """
        self.embeddings = HuggingFaceEmbeddings(model_name=embeddings_model)
        self.k = k
        self.faiss_index = None
        self.bm25_retriever = None

    def _initialize_retrievers(self, documents: List[Document]) -> None:
        """Inicializa os retrievers BM25 e FAISS com os documentos fornecidos."""
        # Inicializa retriever BM25
        self.bm25_retriever = BM25Retriever.from_documents(documents)
        self.bm25_retriever.k = self.k * 2  # Busca mais documentos inicialmente

        # Inicializa index FAISS
        self.faiss_index = FAISS.from_documents(documents, self.embeddings)
        faiss_retriever = self.faiss_index.as_retriever(search_kwargs={"k": self.k * 2})

        # Cria ensemble retriever
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.bm25_retriever, faiss_retriever],
            weights=[0.5, 0.5]
        )

    def _mmr(self, query_embedding: np.ndarray, documents: List[Document],
             lambda_param: float = 0.5, top_n: int = 5) -> List[Document]:
        """
        Implementa o algoritmo MMR para seleção de documentos.

        Args:
            query_embedding: Embedding da query
            documents: Lista de documentos candidatos
            lambda_param: Parâmetro de balanceamento (0 = diversidade pura, 1 = relevância pura)
            top_n: Número de documentos a retornar

        Returns:
            Lista dos documentos mais relevantes e diversos
        """
        if not documents:
            return []

        # Calcula similaridade com a query
        doc_embeddings = np.array([doc.embedding for doc in documents if doc.embedding is not None])
        if len(doc_embeddings) == 0:
            return []

        query_doc_sim = cosine_similarity([query_embedding], doc_embeddings)[0]

        # Calcula similaridade entre documentos
        doc_doc_sim = cosine_similarity(doc_embeddings)

        selected_indices = []
        candidates = set(range(len(documents)))

        while len(selected_indices) < min(top_n, len(documents)) and candidates:
            # Se nenhum documento foi selecionado ainda, escolhe o mais relevante
            if not selected_indices:
                mmr_scores = query_doc_sim
            else:
                # Calcula MMR para cada candidato
                mmr_scores = []
                for i in candidates:
                    # Relevância média com a query
                    rel = query_doc_sim[i]

                    # Diversidade média com os já selecionados
                    div = np.mean([1 - doc_doc_sim[i][j] for j in selected_indices])

                    # Score MMR
                    mmr_scores.append(lambda_param * rel - (1 - lambda_param) * div)

            # Seleciona o documento com maior score MMR
            best_idx = np.argmax(mmr_scores)
            selected_indices.append(best_idx)
            candidates.remove(best_idx)

        # Retorna os documentos selecionados
        return [documents[i] for i in selected_indices]

    def retrieve(self, query: str, documents: List[Document], lambda_param: float = 0.5) -> List[Document]:
        """
        Recupera documentos relevantes e diversos usando MMR.

        Args:
            query: Consulta do usuário
            documents: Lista de documentos candidatos
            lambda_param: Parâmetro de balanceamento

        Returns:
            Lista de documentos ordenados por relevância e diversidade
        """
        if not documents:
            return []

        # Inicializa retrie