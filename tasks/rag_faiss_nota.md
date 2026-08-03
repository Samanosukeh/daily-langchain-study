```markdown
# FAISS: Otimizando Indexações com `IndexIVFFlat`

## Introdução
O `IndexIVFFlat` é uma variante do **IVF (Inverted File Index)** no FAISS, projetado para indexar vetores de alta dimensão com eficiência em buscas aproximadas. Diferente do `IndexFlatL2` (busca exata), o `IVFFlat` particiona o espaço vetorial em *clusters* (células) usando um algoritmo como o **k-means**, reduzindo o custo computacional da busca.

---

## Parâmetros Críticos
- **`nlist`**: Número de células (clusters) criadas. Um valor alto melhora a precisão, mas aumenta o uso de memória.
- **`nprobe`**: Quantas células são examinadas durante a busca. Valores típicos: 1–100 (trade-off entre velocidade e precisão).
- **`quantizer`**: Algoritmo usado para particionar os vetores (ex: `L2` ou `IP` para distância euclidiana ou produto interno).

---

## Exemplo Prático
```python
import faiss
import numpy as np

# Dados de exemplo (100 vetores de 64 dimensões)
d = 64
nb = 100
xb = np.random.random((nb, d)).astype('float32')

# Configuração do índice IVFFlat
nlist = 5  # Número de células
quantizer = faiss.IndexFlatL2(d)  # Quantizador L2
index = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_L2)

# Treinamento (ajusta os centroides das células)
index.train(xb)
index.add(xb)  # Adiciona vetores ao índice

# Busca aproximada
nprobe = 2  # Examina 2 células
index.nprobe = nprobe
query = np.random.random((1, d)).astype('float32')
D, I = index.search(query, k=3)  # Top-3 resultados
```

---

## Vantagens e Limitações
✅ **Vantagens**:
- Busca **~10–100x mais rápida** que `IndexFlatL2` para grandes datasets.
- Suporte a **GPU** via `IndexIVFFlatGPU` (FAISS-GPU).

❌ **Limitações**:
- **Perda de precisão**: Resultados são aproximados.
- **Sensível ao treinamento**: Células mal definidas degradam desempenho.

---
## Dicas de Otimização
1. **Escolha `nlist`**: Regra prática: `nlist ≈ sqrt(nb)` (ex: para 1M vetores, use ~1000 células).
2. **Ajuste `nprobe`**: Comece com `nprobe=1` e aumente até atingir a precisão desejada.
3. **Re-treinamento**: Atualize o índice periodicamente se os dados mudarem significativamente.

---
## Referências
- [FAISS IVF Documentation](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes#IVF-indexes)
- Paper: *"Billion-scale similarity search with GPUs"* (Johnson et al., 2017).
```