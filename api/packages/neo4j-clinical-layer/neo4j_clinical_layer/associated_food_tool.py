from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

from neo4j_clinical_layer.utils import graph

associated_food_query = """
MATCH (f:Food)-[r:HAS_CONTENT]->(m:Metabolite)-[r2:ASSOCIATED_WITH]->(d:Disease)
WHERE d.name contains $disease
RETURN f.name as name, m.name as metabolite_name, d.name as disease
LIMIT 10
"""


def get_associated_food(disease: str) -> str:
    data = graph.query(associated_food_query, params={"disease": disease})
    return data


class AssociatedFoodInput(BaseModel):
    disease: str = Field(description="disease mentioned in the question")


class AssociatedFoodTool(BaseTool):
    name = "AssociatedFood"
    description = "useful for when you need to find associated foods or metabolites with a given disease"
    args_schema: Type[BaseModel] = AssociatedFoodInput

    def _run(
        self,
        disease: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return get_associated_food(disease)

    async def _arun(
        self,
        disease: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return get_associated_food(disease)
