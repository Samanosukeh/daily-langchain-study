```python
from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain.tools import BaseTool
import requests

class DuckDuckGoSchema(BaseModel):
    query: str = Field(..., description="Consulta de busca para o DuckDuckGo")

class DuckDuckGoSearchTool(BaseTool):
    name = "DuckDuckGo Search"
    description = "Ferramenta para realizar buscas na web usando o motor do DuckDuckGo"
    args_schema: Type[BaseModel] = DuckDuckGoSchema

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Executa a busca síncrona no DuckDuckGo"""
        try:
            url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Erro ao buscar: {str(e)}"

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Executa a busca assíncrona no DuckDuckGo"""
        return self._run(query)
```