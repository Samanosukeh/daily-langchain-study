```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from typing import List
from langchain_core.vectorstores import VectorStore

class SelfQueryRetriever(BaseRetriever):
    def __init__(self, vectorstore: VectorStore):
        self.vectorstore = vectorstore

    def get_relevant_documents(self, query: str) -> List[Document]:
        # Extrai metadados da query (ex: "filme de ação lançado em 2020")
        metadata_filter = self._parse_query_to_metadata(query)

        # Busca no vetorstore com filtro
        docs = self.vectorstore.similarity_search(
            query,
            filter=metadata_filter
        )
        return docs

    def _parse_query_to_metadata(self, query: str) -> dict:
        # Parser simples para extração de metadados (melhorar com NLP real)
        metadata = {}
        if "ação" in query.lower():
            metadata["genre"] = "ação"
        if "2020" in query:
            metadata["year"] = 2020
        return metadata

# Exemplo de uso
if __name__ == "__main__":
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import HuggingFaceEmbeddings

    # Criar embeddings e vetorstore
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    documents = [
        Document(page_content="Matrix", metadata={"genre": "ação", "year": 1999}),
        Document(page_content="Duro de Matar", metadata={"genre": "ação", "year": 1988}),
        Document(page_content="Interestelar", metadata={"genre": "ficção científica", "year": 2014}),
    ]
    vectorstore = FAISS.from_documents(documents, embeddings)

    # Criar retriever
    retriever = SelfQueryRetriever(vectorstore)

    # Busca com filtro implícito
    results = retriever.get_relevant_documents("filme de ação lançado em 2020")
    print(f"Documentos encontrados: {len(results)}")
    for doc in results:
        print(f"- {doc.page_content} ({doc.metadata})")
```