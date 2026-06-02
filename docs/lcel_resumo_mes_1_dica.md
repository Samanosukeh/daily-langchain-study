```markdown
# **Resumo Mês 1: Do LLM Call à Chains em LangChain**

## **📌 Fundamentos de LLM Call**
- Use `langchain.llms` para integração com modelos (OpenAI, HuggingFace, etc.).
- Exemplo básico:
  ```python
  from langchain.llms import OpenAI
  llm = OpenAI(model_name="text-davinci-003")
  response = llm("Qual é a capital do Brasil?")
  ```

## **🔗 Prompts e Templates**
- Crie prompts reutilizáveis com `PromptTemplate`:
  ```python
  from langchain.prompts import PromptTemplate
  template = "Resuma o texto: {texto}"
  prompt = PromptTemplate.from_template(template)
  ```

## **📝 Output Parsers**
- Extraia dados estruturados com `OutputParser`:
  ```python
  from langchain.output_parsers import CommaSeparatedListOutputParser
  output_parser = CommaSeparatedListOutputParser()
  parsed = output_parser.parse("maçã, banana, laranja")
  ```

## **🔗 Chains Básicas**
- Combine LLM + Prompt + Parser em uma cadeia (`LLMChain`):
  ```python
  from langchain.chains import LLMChain
  chain = LLMChain(llm=llm, prompt=prompt, output_parser=output_parser)
  result = chain.run(texto="Python é uma linguagem de programação.")
  ```

## **📌 Document Loaders**
- Carregue dados externos com `DocumentLoader`:
  ```python
  from langchain.document_loaders import TextLoader
  loader = TextLoader("arquivo.txt")
  docs = loader.load()
  ```

## **🔍 Text Splitters**
- Divida textos longos para processamento:
  ```python
  from langchain.text_splitter import CharacterTextSplitter
  splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=20)
  chunks = splitter.split_documents(docs)
  ```

## **📊 Vector Stores (Próximos Passos)**
- Armazene embeddings para busca semântica (ex: `FAISS`, `Chroma`).
- Exemplo:
  ```python
  from langchain.vectorstores import FAISS
  db = FAISS.from_documents(chunks, embeddings)
  ```

---
**💡 Dica Final**: Documente cada etapa e teste incrementalmente!
```