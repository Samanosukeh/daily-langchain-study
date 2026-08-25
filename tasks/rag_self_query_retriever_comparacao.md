```markdown
# Self-Query Retriever vs. Retrieval Tradicional

## **Self-Query Retriever**
- **Funcionamento**: O LLM gera *queries estruturadas* (ex: filtros SQL-like) dinamicamente com base na pergunta do usuário.
- **Vantagens**:
  - **Precisão**: Recupera documentos relevantes mesmo com perguntas ambíguas.
  - **Flexibilidade**: Suporta filtros complexos (ex: `data > 2023 AND categoria = "tecnologia"`).
  - **Redução de ruído**: Filtra documentos irrelevantes antes da recuperação.
- **Desvantagens**:
  - **Dependência do LLM**: Erros na geração da query impactam diretamente os resultados.
  - **Complexidade**: Requer schema definido (ex: metadados dos documentos).
- **Casos de uso**:
  - Buscas em bases de dados com metadados ricos.
  - Sistemas onde a pergunta do usuário é genérica, mas os dados são estruturados.

---

## **Retrieval Tradicional (Ex: Vector Search)**
- **Funcionamento**: Busca por similaridade vetorial (ex: embeddings) sem interpretação semântica da query.
- **Vantagens**:
  - **Simplicidade**: Não depende de schema ou geração de queries.
  - **Performance**: Rápido para buscas em grandes datasets não estruturados.
- **Desvantagens**:
  - **Ruído**: Retorna documentos semanticamente próximos, mas não necessariamente relevantes.
  - **Limitações**: Não filtra por metadados sem lógica adicional.
- **Casos de uso**:
  - Buscas em documentos não estruturados (ex: artigos de texto puro).
  - Sistemas onde a similaridade vetorial é suficiente.

---

## **Comparação Direta**
| Critério               | Self-Query Retriever       | Retrieval Tradicional       |
|------------------------|----------------------------|-----------------------------|
| **Dependência do LLM** | Alta (precisa de prompt)   | Baixa                       |
| **Precisão em filtros**| Alta                       | Baixa                       |
| **Complexidade**       | Alta (schema necessário)   | Baixa                       |
| **Performance**        | Média (depende do LLM)     | Alta                        |
| **Flexibilidade**      | Alta (queries dinâmicas)   | Baixa                       |

---
**Conclusão**:
- Use **Self-Query Retriever** quando os dados tiverem metadados ricos e a pergunta do usuário for ambígua.
- Use **Retrieval Tradicional** para buscas rápidas em dados não estruturados.
```