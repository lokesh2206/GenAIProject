"""
Table Dependencies Agent
"""
from typing import Dict, Any, List
from core.llm_provider import LLMProvider
from config.settings import settings

class DependencyAgent:
    """Agent for analyzing table dependencies"""
    
    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize Dependency Agent
        
        Args:
            llm_provider: LLM provider instance
        """
        self.llm = llm_provider
        self.system_prompt = settings.DEPENDENCY_AGENT_PROMPT
    
    def analyze_dependencies(
        self,
        schema_context: str,
        additional_tables: str = ""
    ) -> Dict[str, Any]:
        """
        Analyze table dependencies and relationships
        
        Args:
            schema_context: Schema information
            additional_tables: Optional information about other tables
            
        Returns:
            Dictionary with dependency analysis and recommendations
        """
        prompt = f"""Analyze the following schema and identify table dependencies and relationships:

Schema:
{schema_context}

{f"Additional Tables Context: {additional_tables}" if additional_tables else ""}

Provide analysis on:
1. Primary Key Candidates - Columns that could serve as primary keys
2. Foreign Key Relationships - Potential relationships with other tables
3. Join Strategies - Recommended join types and conditions
4. Dependency Graph - Visual representation of dependencies
5. Data Lineage - How data flows between tables
6. Normalization Analysis - Current normalization level and recommendations

For each relationship identified, provide:
- Source and target tables/columns
- Relationship type (1:1, 1:N, N:M)
- Join condition
- Cardinality estimate

If possible, provide a Mermaid diagram for the dependency graph.
"""
        
        try:
            response = self.llm.generate(prompt, system_message=self.system_prompt)
            
            # Extract relationships
            relationships = self._extract_relationships(response)
            
            # Extract mermaid diagram if present
            mermaid_diagram = self._extract_mermaid(response)
            
            return {
                "dependency_analysis": response,
                "relationships": relationships,
                "mermaid_diagram": mermaid_diagram,
                "summary": self._generate_summary(relationships)
            }
        except Exception as e:
            return {
                "error": str(e),
                "dependency_analysis": "",
                "relationships": [],
                "mermaid_diagram": "",
                "summary": ""
            }
    
    def _extract_relationships(self, response: str) -> List[Dict[str, str]]:
        """Extract relationships from response"""
        # Simplified extraction - in production, use more robust parsing
        relationships = []
        
        # Look for common relationship indicators
        if "Foreign Key" in response or "foreign key" in response:
            relationships.append({
                "type": "foreign_key",
                "description": "See full response for details"
            })
        
        if "Primary Key" in response or "primary key" in response:
            relationships.append({
                "type": "primary_key",
                "description": "See full response for details"
            })
        
        return relationships
    
    def _extract_mermaid(self, response: str) -> str:
        """Extract Mermaid diagram from response"""
        try:
            if "```mermaid" in response:
                start = response.find("```mermaid") + 10
                end = response.find("```", start)
                return response[start:end].strip()
            return ""
        except:
            return ""
    
    def _generate_summary(self, relationships: List[Dict[str, str]]) -> str:
        """Generate a summary of dependencies"""
        if not relationships:
            return "No explicit relationships identified"
        
        return f"Identified {len(relationships)} potential relationships"
