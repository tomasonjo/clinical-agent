from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

from neo4j_clinical_layer.utils import graph

gene_clinical_query = """
MATCH (p:Protein)-[r:ASSOCIATED_WITH]-(d:Disease) 
WHERE d.name CONTAINS $disease
OPTIONAL MATCH (p)-[r2:ASSOCIATED_WITH]->(t:Tissue)
RETURN d.name as disease, p.name as drug_target, t.name as expressed_tissue
LIMIT 10
"""


def get_disease_tissue_expression(disease: str) -> str:
    data = graph.query(gene_clinical_query, params={"disease": disease})
    return data


class DiseaseTissueInput(BaseModel):
    disease: str = Field(description="disease mentioned in the question")


class DiseaseTissueTool(BaseTool):
    name = "DiseaseTissue"
    description = "useful for when you need to find tissues where proteins with a specific disease are expressed"
    args_schema: Type[BaseModel] = DiseaseTissueInput

    def _run(
        self,
        disease: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return get_disease_tissue_expression(disease)

    async def _arun(
        self,
        disease: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return get_disease_tissue_expression(disease)
