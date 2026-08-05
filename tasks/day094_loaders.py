```python
# tasks/data_loaders.py

from langchain.document_loaders import TextLoader, CSVLoader
from typing import List, Union
import os

def load_text_file(file_path: str) -> List[str]:
    """
    Carrega o conteúdo de um arquivo de texto usando TextLoader.

    Args:
        file_path (str): Caminho para o arquivo .txt

    Returns:
        List[str]: Lista de documentos carregados
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    loader = TextLoader(file_path)
    documents = loader.load()
    return documents

def load_csv_file(file_path: str, encoding: str = "utf-8") -> List[str]:
    """
    Carrega dados de um arquivo CSV usando CSVLoader.

    Args:
        file_path (str): Caminho para o arquivo .csv
        encoding (str): Codificação do arquivo (padrão: utf-8)

    Returns:
        List[str]: Lista de documentos carregados
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    loader = CSVLoader(file_path, encoding=encoding)
    documents = loader.load()
    return documents

def load_document(file_path: str) -> Union[List[str], None]:
    """
    Carrega documentos automaticamente com base na extensão do arquivo.

    Args:
        file_path (str): Caminho para o arquivo (.txt ou .csv)

    Returns:
        Union[List[str], None]: Lista de documentos ou None se extensão não suportada
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        return load_text_file(file_path)
    elif ext == ".csv":
        return load_csv_file(file_path)
    else:
        print(f"Extensão {ext} não suportada para carregamento automático.")
        return None
```