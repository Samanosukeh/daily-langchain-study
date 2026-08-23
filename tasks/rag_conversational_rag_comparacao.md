```markdown
# **Conversational RAG vs. RAG Tradicional: Comparação**

## **1. Histórico e Conceito Base**
- **RAG Tradicional**:
  - Introduzido em 2020 como forma de melhorar LLMs com conhecimento externo.
  - Focado em **recuperação + geração** em um único passo.
  - Pipeline linear: `Query → Busca → Geração`.

- **Conversational RAG**:
  - Evolução natural para **diálogos multi-turno** (ex: Chatbots).
  - Adiciona **memória contextual** e **adaptação dinâmica**.
  - Pipeline iterativo: `Query → Busca → Geração → Memória → Próxima Query`.

---

## **2. Arquitetura Comparada**
| **Aspecto**          | **RAG Tradicional**               | **Conversational RAG**            |
|----------------------|-----------------------------------|-----------------------------------|
| **Recuperação**      | Busca estática (sem contexto)     | Busca com histórico de diálogos   |
| **Memória**          | Inexistente                       | Short/Long-term memory (ex: vetores) |
| **Geração**          | Resposta única                    | Respostas adaptativas ao contexto |
| **Feedback Loop**    | Ausente                           | Integração com reforço humano     |
| **Complexidade**     | Baixa                             | Alta (precisa de orquestração)    |

---

## **3. Casos de Uso**
- **RAG Tradicional**:
  - Perguntas factuais (ex: "Qual a capital da França?").
  - Documentação técnica (busca em manuais).

- **Conversational RAG**:
  - Assistentes médicos (histórico do paciente).
  - Suporte técnico multi-turno (ex: "Como reiniciar o servidor? → Mas antes, qual é o modelo?").

---
## **4. Desafios**
- **RAG Tradicional**:
  - Limitações em perguntas ambíguas.
  - Sem aprendizado incremental.

- **Conversational RAG**:
  - Custo computacional alto (memória + LLMs).
  - Gerenciamento de contexto (ex: *hallucinations* em diálogos longos).
  - Dependência de frameworks como LangChain/LangGraph.

---
## **5. Ferramentas para Implementar**
- **RAG Tradicional**:
  - `FAISS`/`Chroma` (vetorização).
  - `LangChain` (pipeline básico).

- **Conversational RAG**:
  - `LangGraph` (para workflows complexos).
  - `Redis`/`PostgreSQL` (armazenamento de memória).
  - `LlamaIndex` (para indexação hierárquica).

---
## **6. Quando Usar Cada Um?**
- **Use RAG Tradicional** se:
  - Precisa de respostas rápidas e pontuais.
  - Não há necessidade de contexto histórico.

- **Use Conversational RAG** se:
  - O usuário interage em múltiplos turnos.
  - A precisão depende de histórico (ex: assistentes pessoais).
```