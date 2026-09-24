```markdown
# **Resumo Mês 5: Avaliação de Sistemas com LangChain**

## **1. Métricas Essenciais**
- **Precisão (Accuracy)**: % de respostas corretas.
- **Recall**: Capacidade de recuperar informações relevantes.
- **F1-Score**: Média harmônica entre precisão e recall.
- **Latência**: Tempo de resposta do sistema (ideal < 2s).

## **2. Ferramentas de Avaliação**
- **LangChain Evaluation**: Usar `langchain.evaluation` para testes automatizados.
- **PromptTemplates**: Validar prompts com `StringPromptTemplate`.
- **Chain-of-Thought (CoT)**: Avaliar raciocínio em etapas.

## **3. Testes Práticos**
- **Teste de Stress**: Simular 1000 requisições para medir estabilidade.
- **Teste de Edge Cases**: Perguntas ambíguas ou fora do contexto.
- **Feedback Humano**: Validar respostas com usuários reais.

## **4. Otimizações**
- **Cache de Respostas**: Usar `InMemoryCache` para reduzir custos.
- **Ajuste de Parâmetros**: Temperatura (`temperature`) entre 0.1 e 0.7.
- **Fallbacks**: Implementar respostas padrão para erros.

## **5. Documentação**
- **Logs Detalhados**: Registrar tempo de resposta e tokens usados.
- **Relatórios Automatizados**: Gerar PDFs com métricas via `reportlab`.
- **Versionamento**: Usar Git para rastrear mudanças nos prompts.

---
**Dica Final**: Sempre valide com um **dataset de referência** antes de deploy.
```