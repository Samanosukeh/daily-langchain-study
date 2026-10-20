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

---

```markdown
# Comentários no Agent de Q&A

## Visão Geral
Este documento descreve como implementar e gerenciar comentários em um **Agent de Q&A** usando LangChain, focando no projeto `tas...`.

---

## Estrutura de Comentários

### 1. Tipo de Comentários Suportados
- **Feedback do usuário**: Avaliações ou sugestões sobre respostas geradas.
- **Notas internas**: Comentários para desenvolvimento ou depuração.
- **Contexto histórico**: Registros de interações anteriores.

### 2. Implementação Básica
```python
from langchain.schema import AgentOutputParser

class QACommentParser(AgentOutputParser):
    def parse(self, output: str) -> dict:
        """
        Extrai comentários do output do agent.
        Exemplo de formato esperado:
        {
            "resposta": "Texto da resposta",
            "comentarios": [
                {"tipo": "feedback", "texto": "Resposta clara"},
                {"tipo": "nota", "texto": "Revisar fonte X"}
            ]
        }
        """
        # Lógica de parsing aqui
        return parsed_data
```

---

## Integração com o Agent

### 1. Configuração do Agent
```python
from langchain.agents import initialize_agent

agent = initialize_agent(
    tools=[...],
    agent=...,
    output_parser=QACommentParser(),
    verbose=True
)
```

### 2. Tratamento de Comentários
```python
def process_output(output: dict):
    """Processa comentários e gera ações correspondentes."""
    for comment in output.get("comentarios", []):
        if comment["tipo"] == "feedback":
            log_feedback(comment["texto"])
        elif comment["tipo"] == "nota":
            notify_team(comment["texto"])
```

---

## Boas Práticas

1. **Formato Padronizado**:
   - Use JSON ou YAML para estruturar comentários.
   - Exemplo:
     ```json
     {
         "resposta": "...",
         "comentarios": [
             {"tipo": "feedback", "nota": 5, "texto": "..."}
         ]
     }
     ```

2. **Armazenamento**:
   - Salve comentários em banco de dados (ex: SQLite, PostgreSQL).
   - Exemplo de tabela:
     ```sql
     CREATE TABLE comentarios (
         id INTEGER PRIMARY KEY,
         tipo TEXT,
         texto TEXT,
         resposta_id INTEGER,
         FOREIGN KEY (resposta_id) REFERENCES respostas(id)
     );
     ```

3. **Validação**:
   - Valide comentários antes de processá-los:
     ```python
     from pydantic import BaseModel, validator

     class Comentario(BaseModel):
         tipo: str
         texto: str

         @validator("tipo")
         def validar_tipo(cls, v):
             if v not in ["feedback", "nota", "historico"]:
                 raise ValueError("Tipo de comentário inválido")
             return v
     ```

---

## Exemplo Completo

```python
from langchain.agents import AgentExecutor
from langchain.chains import LLMChain

# Configuração
llm_chain = LLMChain(llm=..., prompt=...)
output_parser = QACommentParser()
agent = AgentExecutor(llm_chain=llm_chain, output_parser=output_parser)

# Execução
output = agent.run("Qual a capital da França?")
process_output(output)
```

---

## Referências
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [Pydantic Validators](https://pydantic-docs.helpmanual.io/)
```