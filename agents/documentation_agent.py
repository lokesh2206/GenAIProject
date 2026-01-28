"""
Documentation Generation Agent
"""
from typing import Dict, Any
from core.llm_provider import LLMProvider
from config.settings import settings

class DocumentationAgent:
    """Agent for generating dataset documentation"""
    
    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize Documentation Agent
        
        Args:
            llm_provider: LLM provider instance
        """
        self.llm = llm_provider
        self.system_prompt = settings.DOCUMENTATION_AGENT_PROMPT
    
    def generate_documentation(
        self,
        schema_context: str,
        doc_type: str = "data_dictionary"
    ) -> Dict[str, Any]:
        """
        Generate documentation for the dataset
        
        Args:
            schema_context: Schema information
            doc_type: Type of documentation (data_dictionary, readme, schema_doc)
            
        Returns:
            Dictionary with generated documentation
        """
        if doc_type == "data_dictionary":
            return self._generate_data_dictionary(schema_context)
        elif doc_type == "readme":
            return self._generate_readme(schema_context)
        elif doc_type == "schema_doc":
            return self._generate_schema_doc(schema_context)
        else:
            return {"error": f"Unknown documentation type: {doc_type}"}
    
    def _generate_data_dictionary(self, schema_context: str) -> Dict[str, Any]:
        """Generate data dictionary"""
        prompt = f"""Generate a comprehensive data dictionary for the following dataset:

{schema_context}

The data dictionary should include:
1. Table/Dataset Overview
2. Column Definitions Table with:
   - Column Name
   - Data Type
   - Description
   - Constraints (nullable, unique, etc.)
   - Sample Values
   - Business Meaning
3. Data Quality Notes
4. Usage Guidelines

Format the output in Markdown with proper tables and formatting.
"""
        
        try:
            response = self.llm.generate(prompt, system_message=self.system_prompt)
            
            return {
                "documentation": response,
                "doc_type": "data_dictionary",
                "format": "markdown"
            }
        except Exception as e:
            return {
                "error": str(e),
                "documentation": "",
                "doc_type": "data_dictionary"
            }
    
    def _generate_readme(self, schema_context: str) -> Dict[str, Any]:
        """Generate README file"""
        prompt = f"""Generate a README.md file for the following dataset:

{schema_context}

The README should include:
1. Dataset Title and Description
2. Data Source and Collection Method
3. Schema Overview
4. Key Statistics
5. Usage Examples
6. Data Quality Notes
7. Update Frequency
8. Contact Information (placeholder)

Format the output in Markdown.
"""
        
        try:
            response = self.llm.generate(prompt, system_message=self.system_prompt)
            
            return {
                "documentation": response,
                "doc_type": "readme",
                "format": "markdown"
            }
        except Exception as e:
            return {
                "error": str(e),
                "documentation": "",
                "doc_type": "readme"
            }
    
    def _generate_schema_doc(self, schema_context: str) -> Dict[str, Any]:
        """Generate schema documentation"""
        prompt = f"""Generate technical schema documentation for the following dataset:

{schema_context}

The schema documentation should include:
1. Schema Version and Last Updated
2. Detailed Column Specifications
3. Data Types and Precision
4. Indexes and Constraints
5. Relationships and Dependencies
6. Performance Considerations
7. Migration Notes

Format the output in Markdown with technical details.
"""
        
        try:
            response = self.llm.generate(prompt, system_message=self.system_prompt)
            
            return {
                "documentation": response,
                "doc_type": "schema_doc",
                "format": "markdown"
            }
        except Exception as e:
            return {
                "error": str(e),
                "documentation": "",
                "doc_type": "schema_doc"
            }
