```markdown
# Resumo Mês 5: Avaliação de Sistemas LLM

## Tópicos Abordados
- **Evaluation Frameworks**
- **Métricas de Avaliação**
- **Arquiteturas de Comparação**
- **Benchmarking**

---

## 1. Evaluation Frameworks
Ferramentas e bibliotecas para avaliar modelos de linguagem:

```python
# Exemplo com LangChain Evaluation
from langchain.evaluation import load_evaluator

evaluator = load_evaluator("qa", evaluator_type="criteria")
result = evaluator.evaluate(
    input="Qual é a capital do Brasil?",
    prediction="Brasília",
    criteria={"correctness": "A resposta deve ser correta."}
)
print(result)
```

### Frameworks Populares:
- **LangChain Evaluation** (LangSmith)
- **Hugging Face Evaluate**
- **RAGAS** (para RAG)
- **DeepEval**

---

## 2. Métricas de Avaliação
Métricas comuns para LLM:

| Métrica          | Descrição                          | Exemplo de Uso                     |
|------------------|------------------------------------|------------------------------------|
| **Acurácia**     | Precisão das respostas             | Comparar com ground truth          |
| **BLEU/ROUGE**   | Similaridade com texto de referência| Avaliar tradução ou resumo         |
| **F1-Score**     | Equilíbrio precisão/recall         | Classificação de intenções         |
| **Perplexity**   | Qualidade da distribuição de tokens | Avaliar fluência do modelo         |
| **Latência**     | Tempo de resposta                  | Otimização de sistemas em produção |

```python
# Exemplo com RAGAS (para RAG)
from ragas import evaluate
from datasets import Dataset

dataset = Dataset.from_dict({
    "question": ["Qual é a capital do Brasil?"],
    "answer": ["Brasília"],
    "contexts": [["O Brasil é um país da América do Sul."]],
    "ground_truth": ["Brasília"]
})

result = evaluate(dataset)
print(result)
```

---

## 3. Arquiteturas de Comparação
Comparação entre modelos ou abordagens:

### Abordagens:
1. **Head-to-Head**: Comparar dois modelos diretamente.
   ```python
   from langchain.evaluation import compare

   compare(
       prediction1="Resposta A",
       prediction2="Resposta B",
       input="Pergunta de teste",
       model="gpt-3.5-turbo"
   )
   ```
2. **A/B Testing**: Testar versões diferentes de um sistema.
3. **Human-in-the-Loop**: Avaliação humana com feedback.

### Ferramentas:
- **LangSmith** (para comparação de traces)
- **Weights & Biases** (para experiment tracking)
- **MLflow** (para versionamento)

---

## 4. Benchmarking
Avaliação em datasets padronizados:

### Datasets Comuns:
- **MMLU** (Massive Multitask Language Understanding)
- **TruthfulQA** (Avaliar tendências de respostas)
- **SQuAD** (para perguntas e respostas)
- **HellaSwag** (compreensão de contexto)

### Exemplo com MMLU:
```python
from langchain.evaluation import MMLUEvaluator

evaluator = MMLUEvaluator(model="gpt-3.5-turbo")
result = evaluator.evaluate(
    subject="elementary_mathematics",
    input="Qual é a soma de 2 + 2?"
)
print(result)
```

### Ferramentas de Benchmark:
- **EleutherAI LM Evaluation Harness**
- **Hugging Face Open LLM Leaderboard**

---

## Boas Práticas
1. **Definir objetivos claros**: O que você quer avaliar? (ex: coerência, precisão, criatividade)
2. **Usar múltiplas métricas**: Não dependa de apenas uma.
3. **Incluir avaliação humana**: Para métricas subjetivas (ex: tom, estilo).
4. **Automatizar o processo**: Use pipelines de CI/CD para testes contínuos.
5. **Documentar resultados**: Para reprodutibilidade.

---

## Ferramentas Recomendadas
| Ferramenta               | Uso Principal                          |
|--------------------------|----------------------------------------|
| **LangSmith**            | Avaliação de traces e comparações     |
| **RAGAS**                | Avaliação de sistemas RAG              |
| **DeepEval**             | Métricas personalizadas               |
| **Weights & Biases**     | Experiment tracking e visual