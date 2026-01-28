"""
Data Quality Rules Agent
"""
from typing import Dict, Any, List
from core.llm_provider import LLMProvider
from config.settings import settings

class QualityAgent:
    """Agent for generating data quality rules"""
    
    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize Quality Agent
        
        Args:
            llm_provider: LLM provider instance
        """
        self.llm = llm_provider
        self.system_prompt = settings.QUALITY_AGENT_PROMPT
    
    def generate_quality_rules(self, schema_context: str) -> Dict[str, Any]:
        """
        Generate data quality rules based on schema
        
        Args:
            schema_context: Schema information
            
        Returns:
            Dictionary with quality rules and recommendations
        """
        prompt = f"""Analyze the following database schema and generate comprehensive data quality rules:

{schema_context}

Provide data quality rules in the following categories:
1. Null/Completeness Checks - Which columns should not be null
2. Range/Value Checks - Valid ranges for numeric columns
3. Format Checks - Expected formats for string columns (email, phone, etc.)
4. Uniqueness Checks - Columns that should have unique values
5. Referential Integrity - Potential foreign key relationships
6. Business Logic Rules - Domain-specific validation rules

For each rule, provide:
- Rule name
- Description
- SQL validation query (if applicable)
- Severity (Critical, High, Medium, Low)

Format your response clearly with headers for each category.
"""
        
        try:
            response = self.llm.generate(prompt, system_message=self.system_prompt)
            
            # Parse the response into structured format
            rules = self._parse_quality_rules(response)
            
            return {
                "quality_rules": rules,
                "full_response": response,
                "summary": self._generate_summary(rules)
            }
        except Exception as e:
            return {
                "error": str(e),
                "quality_rules": [],
                "full_response": "",
                "summary": ""
            }
    
    def _parse_quality_rules(self, response: str) -> List[Dict[str, str]]:
        """Parse quality rules from response"""
        # This is a simplified parser - in production, you'd want more robust parsing
        rules = []
        
        categories = [
            "Null/Completeness Checks",
            "Range/Value Checks",
            "Format Checks",
            "Uniqueness Checks",
            "Referential Integrity",
            "Business Logic Rules"
        ]
        
        for category in categories:
            if category in response:
                rules.append({
                    "category": category,
                    "content": "See full response for details"
                })
        
        return rules
    
    def _generate_summary(self, rules: List[Dict[str, str]]) -> str:
        """Generate a summary of quality rules"""
        if not rules:
            return "No quality rules generated"
        
        return f"Generated {len(rules)} categories of data quality rules"
