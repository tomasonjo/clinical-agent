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
MATCH(g:Gene)
WHERE g.id =~ '(?i)' + $gene
WITH g
OPTIONAL MATCH (g)-[r:VARIANT_FOUND_IN_GENE]-(v:Known_variant)
WHERE NOT v.clinical_relevance = '-' AND NOT v.disease = '-'
RETURN g.id as gene, v.disease AS disease, v.pvariant_id AS variant_id, v.clinical_relevance as relevance
LIMIT 20
"""


def get_gene_variant(gene: str) -> str:
    data = graph.query(gene_clinical_query, params={"gene": gene})
    return data


class GeneVariantInput(BaseModel):
    gene: str = Field(description="gene mentioned in the question")


class GeneVariantTool(BaseTool):
    name = "GeneVariant"
    description = (
        "useful for when you need to find clinically relevant variants of a gene"
    )
    args_schema: Type[BaseModel] = GeneVariantInput

    def _run(
        self,
        gene: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        return get_gene_variant(gene)

    async def _arun(
        self,
        gene: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return get_gene_variant(gene)
