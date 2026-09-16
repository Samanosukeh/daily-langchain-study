```markdown
# Avaliação de RAG com Métricas de Fidelidade (Faithfulness)

## Introdução
A métrica **Faithfulness** avalia se as afirmações geradas pelo modelo de RAG são consistentes com o contexto fornecido. Diferente de métricas de similaridade (ex: BLEU, ROUGE), ela foca em **precisão factual** em relação à fonte.

---

## Implementação com LangChain

### 1. Pré-requisitos
```python
from langchain.evaluation import FaithfulnessEvaluator
from langchain_core.documents import Document
```

### 2. Estrutura da Avaliação
- **Entrada**: `prediction` (resposta gerada) + `reference_context` (trecho relevante do documento).
- **Saída**: Escore entre `0` (inconsistente) e `1` (totalmente fiel).

### 3. Exemplo Prático
```python
# Documento de referência (ex: trecho de um artigo)
reference_docs = [
    Document(
        page_content="O Python foi criado por Guido van Rossum em 1991."
    )
]

# Resposta gerada pelo RAG
prediction = "O Python foi criado por Guido van Rossum em 1990."

# Inicializa o avaliador
evaluator = FaithfulnessEvaluator()

# Gera o relatório
result = evaluator.evaluate_strings(
    prediction=prediction,
    input=reference_docs[0].page_content,
)

print(f"Faithfulness Score: {result['score']:.2f}")
# Output: Faithfulness Score: 0.00 (ano incorreto)
```

### 4. Interpretação
- **Score = 1.0**: Resposta 100% fiel ao contexto.
- **Score < 1.0**: Identifica inconsistências (ex: datas, nomes, fatos alterados).

### 5. Limitações
- **Dependência de contexto**: Se o trecho de referência não cobrir a resposta, o score será baixo.
- **Viés de linguagem**: Modelos podem "inventar" detalhes não presentes no contexto.

---

## Boas Práticas
1. **Use trechos relevantes**: Filtre documentos antes da avaliação para focar no contexto necessário.
2. **Combine métricas**: Combine Faithfulness com `AnswerCorrectness` para avaliar precisão e relevância.
3. **Ajuste thresholds**: Defina um score mínimo aceitável (ex: 0.8) para considerar a resposta válida.

---
```