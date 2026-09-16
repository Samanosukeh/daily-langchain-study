```markdown
# Avaliação de LLMs: O Problema de Avaliar Texto

## Introdução

Avaliar modelos de linguagem (LLMs) é um desafio crítico, especialmente quando se trata de métricas de qualidade de texto. Diferente de tarefas tradicionais de machine learning (ex: classificação binária), a avaliação de texto é subjetiva, multidimensional e depende de contexto.

---

## Desafios Principais

### 1. **Subjetividade e Variabilidade Humana**
- **Problema**: O que é considerado um "bom texto" depende de:
  - **Domínio** (ex: técnico vs. criativo).
  - **Audiência** (ex: leigo vs. especialista).
  - **Propósito** (ex: informar vs. entreter).
- **Solução**: Usar **avaliações humanas** (ex: *Human Evaluation*) com diretrizes claras.

### 2. **Falta de Métricas Universais**
- **Problema**: Métricas automáticas (ex: BLEU, ROUGE) são limitadas:
  - **BLEU/ROUGE**: Focam em sobreposição de n-gramas, não capturam coerência ou criatividade.
  - **Métricas baseadas em embeddings** (ex: BERTScore): Melhoram a captura semântica, mas ainda são superficiais.
- **Solução**: **Avaliação multidimensional** (ex: fluência, relevância, coerência, criatividade).

### 3. **Bias e Inconsistência**
- **Problema**: Avaliadores humanos podem ser influenciados por:
  - **Bias de posição** (ex: preferência por respostas longas).
  - **Bias de viés cultural/linguístico**.
- **Solução**: **Avaliação cega** (avaliadores não sabem qual modelo gerou o texto) e **diversidade de avaliadores**.

---

## Abordagens de Avaliação

### 1. **Avaliação Humana (Human Evaluation)**
- **Métodos**:
  - **Escalas Likert**: Avaliar atributos em uma escala (ex: 1-5 para "coerência").
  - **Comparação pareada**: Comparar dois textos e escolher o melhor.
  - **Avaliação qualitativa**: Feedback livre sobre aspectos específicos.
- **Ferramentas**:
  - **Amazon Mechanical Turk** (para crowdsourcing).
  - **Label Studio** (para anotação customizada).

### 2. **Métricas Automáticas**
| Métrica          | Descrição                          | Limitações                     |
|------------------|------------------------------------|---------------------------------|
| **BLEU**         | Sobreposição de n-gramas com referência. | Não captura semântica.          |
| **ROUGE**        | Similar ao BLEU, focado em sumarização. | Limitado a tarefas de resumo.   |
| **BERTScore**    | Compara embeddings semânticos.     | Dependente da qualidade do BERT.|
| **Perplexity**   | Mede a incerteza do modelo.        | Não avalia qualidade do texto.  |

### 3. **Avaliação Baseada em Tarefas**
- **Exemplos**:
  - **QA (Question Answering)**: Avaliar acurácia e relevância das respostas.
  - **Sumarização**: Avaliar fidelidade ao texto original.
  - **Geração criativa**: Avaliar originalidade e coerência.
- **Ferramentas**:
  - **HELM** (Holistic Evaluation of Language Models).
  - **Big-Bench** (coleção de benchmarks).

### 4. **Avaliação de Robustez e Segurança**
- **Testes**:
  - **Prompt Injection**: Verificar se o modelo rejeita prompts maliciosos.
  - **Bias**: Avaliar se o modelo gera conteúdo discriminatório.
  - **Alucinações**: Verificar se o modelo inventa fatos.
- **Ferramentas**:
  - **TruthfulQA** (para testar alucinações).
  - **Bias Benchmarks** (ex: BBQ, StereoSet).

---

## Boas Práticas

1. **Combine métodos**: Use avaliação humana + métricas automáticas.
2. **Seja transparente**: Documente metodologia e limitações.
3. **Iterativo**: Melhore a avaliação com feedback contínuo.
4. **Padronize**: Use protocolos claros para reduzir viés.
5. **Avalie contexto**: Um