```markdown
# Instalação e Configuração do Ambiente

## Pré-requisitos

- **Python**: Versão 3.8 ou superior
  ```bash
  python --version
  ```
  Se não estiver instalado:
  - **Linux/macOS**:
    ```bash
    sudo apt update && sudo apt install python3 python3-pip
    ```
  - **Windows**:
    Baixe em [python.org](https://www.python.org/downloads/)

- **Git** (opcional, para clonar repositórios):
  ```bash
  git --version
  ```
  Instale em [git-scm.com](https://git-scm.com/)

---

## Instalação do LangChain

1. **Crie um ambiente virtual** (recomendado):
   ```bash
   python -m venv langchain_env
   source langchain_env/bin/activate  # Linux/macOS
   langchain_env\Scripts\activate     # Windows
   ```

2. **Instale o LangChain**:
   ```bash
   pip install langchain
   ```

3. **Instale dependências adicionais** (conforme uso):
   - Para integração com LLMs (ex: OpenAI):
     ```bash
     pip install langchain-openai
     ```
   - Para uso com documentos (ex: PyPDF, FAISS):
     ```bash
     pip install pypdf faiss-cpu
     ```

---

## Configuração de Chaves de API

1. **Crie um arquivo `.env`** na raiz do projeto:
   ```plaintext
   OPENAI_API_KEY="sua_chave_aqui"
   # Outras chaves conforme necessário (ex: HUGGINGFACEHUB_API_TOKEN)
   ```

2. **Instale o pacote `python-dotenv`**:
   ```bash
   pip install python-dotenv
   ```

3. **Carregue as variáveis no código**:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

---

## Verificação da Instalação

Execute um teste rápido:
```python
from langchain.llms import OpenAI

llm = OpenAI(temperature=0.9)
print(llm("Qual é a capital do Brasil?"))
```

Saída esperada:
```plaintext
A capital do Brasil é Brasília.
```

---

## Solução de Problemas

- **Erro de versão do Python**:
  Atualize o Python ou crie um ambiente com a versão compatível.

- **Dependências conflitantes**:
  Use `pip install --upgrade` ou reinstale em um ambiente limpo.

- **Chaves de API não carregadas**:
  Verifique se o arquivo `.env` está no diretório correto e o `python-dotenv` foi importado.

---
```