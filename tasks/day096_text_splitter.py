```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Texto de exemplo (substitua pelo seu conteúdo)
texto = """
Título do Documento

Seção 1: Introdução
Esta é a primeira seção do documento. Ela contém informações introdutórias sobre o tema principal.

Seção 2: Desenvolvimento
Aqui está o desenvolvimento do conteúdo. Vamos discutir os principais pontos:
- Ponto A: Detalhes importantes
- Ponto B: Outras considerações

Seção 3: Conclusão
Conclusão do documento com os principais achados.
"""

# Configuração do RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,  # Tamanho do chunk em caracteres
    chunk_overlap=10,  # Overlap entre chunks para contexto
    length_function=len,  # Função para calcular tamanho (pode ser usada len para texto simples)
    separators=["\n\n", "\n", " ", ""]  # Ordem de separação para divisão recursiva
)

# Divisão do texto
chunks = splitter.split_text(texto)

# Exibição dos resultados
print("Número de chunks gerados:", len(chunks))
print("\nChunks gerados:")
for i, chunk in enumerate(chunks, 1):
    print(f"\n--- Chunk {i} ---")
    print(chunk)
    print(f"Tamanho: {len(chunk)} caracteres")
```