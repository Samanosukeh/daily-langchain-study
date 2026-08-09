```markdown
# Estratégias de Chunking: Tamanho e Overlap Ideais

## Introdução
No contexto de RAG (Retrieval-Augmented Generation), o *chunking* é um passo crítico para garantir que os trechos (*chunks*) de texto sejam otimizados para recuperação e geração de resposta. A estratégia de divisão afeta diretamente a qualidade dos resultados.

---

## 1. Tamanho do Chunk

### Fatores a considerar:
- **Contexto semântico**: Chunks muito pequenos podem perder significado; muito grandes, podem incluir ruído.
- **Limitações do modelo**: Modelos de linguagem têm limites de contexto (ex: 4K, 8K, 32K tokens).
- **Tipo de documento**: Textos técnicos (código) vs. narrativos (artigos) exigem abordagens diferentes.

### Recomendações práticas:
| Tipo de Documento       | Tamanho Ideal (tokens) | Tamanho Ideal (caracteres) | Observações                          |
|-------------------------|------------------------|----------------------------|--------------------------------------|
| Código                  | 100–500                | 500–2.500                  | Preservar funções/classes completas. |
| Artigos/Relatórios      | 500–1.000              | 2.500–5.000                | Parágrafos ou seções lógicas.        |
| Transcrições            | 300–800                | 1.500–4.000                | Frases ou turnos de diálogo.         |
| Documentos jurídicos    | 1.000–2.000            | 5.000–10.000               | Cláusulas ou artigos.                |

---

## 2. Overlap entre Chunks

### Por que usar overlap?
- **Coerência contextual**: Garante que informações relevantes não sejam cortadas abruptamente.
- **Melhor recuperação**: Overlaps aumentam a chance de recuperar trechos semânticos completos.

### Configurações recomendadas:
| Overlap (em tokens) | Overlap (em caracteres) | Quando usar                          |
|---------------------|-------------------------|--------------------------------------|
| 10–20% do tamanho do chunk | 10–20% do tamanho do chunk | Documentos técnicos ou estruturados. |
| 20–30%              | 20–30%                  | Textos narrativos ou transcrições.   |
| 0%                  | 0%                      | Somente se o documento for muito curto ou não estruturado. |

---

## 3. Ferramentas e Implementação em LangChain

### Divisores (*Text Splitters*) nativos:
```python
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
    NLTKTextSplitter,
)

# Exemplo com RecursiveCharacterTextSplitter (ajusta para código/texto)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,       # Tamanho do chunk em caracteres
    chunk_overlap=200,     # Overlap em caracteres
    length_function=len,   # Função para medir tamanho (ou len_token para tokens)
)

# Para chunking por tokens (ex: com tiktoken)
from langchain.text_splitter import TokenTextSplitter
splitter = TokenTextSplitter(
    chunk_size=500,        # Tamanho em tokens
    chunk_overlap=100,     # Overlap em tokens
)
```

### Personalização:
- **Divisores especializados**: Use `MarkdownHeaderTextSplitter` para documentos estruturados.
- **Divisores por linguagem**: `PythonCodeTextSplitter` para código.

---

## 4. Boas Práticas

1. **Teste iterativo**: Ajuste tamanho e overlap com base nos resultados do RAG.
2. **Avalie a recuperação**: Use métricas como `MRR` (Mean Reciprocal Rank) ou `Hit Rate`.
3. **Considere o pré-processamento**: Remova ruídos (ex: cabeçalhos, rodapés) antes do chunking.
4. **Documente a estratégia**: Mantenha registros dos parâmetros usados para reprodutibilidade.

---

## 5. Exemplo Prático

### Pipeline completo:
```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Carregar documento
loader = TextLoader