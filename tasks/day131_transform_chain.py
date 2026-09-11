```python
from langchain.chains import TransformChain
from typing import Dict, Any

def transform_input(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função customizada para transformar a entrada antes de passar para a próxima etapa.
    """
    # Exemplo: Adicionar um prefixo ao texto de entrada
    input_data["texto_transformado"] = f"Processado: {input_data.get('texto', '')}"
    return input_data

def transform_output(output_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função customizada para transformar a saída antes de retornar ao usuário.
    """
    # Exemplo: Extrair apenas o campo 'resultado' da saída
    return {"resultado_final": output_data.get("resultado", "")}

# Definindo a TransformChain
transform_chain = TransformChain(
    transform_input_fn=transform_input,
    transform_output_fn=transform_output
)

# Exemplo de uso
entrada = {"texto": "Olá, mundo!"}
saida_intermediaria = transform_chain.run(entrada)
print("Saída intermediária:", saida_intermediaria)

# Supondo que haja uma próxima etapa que processa 'texto_transformado'
# E retorna um dicionário com 'resultado'
proxima_entrada = {"texto": saida_intermediaria["texto_transformado"]}
# Simulando a próxima etapa
proxima_saida = {"resultado": f"Processado: {proxima_entrada['texto']}"}

# Aplicando a transformação de saída
saida_final = transform_chain.apply(proxima_saida)
print("Saída final:", saida_final)
```