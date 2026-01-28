"""
Spark Optimization Agent
"""
from typing import Dict, Any
from core.llm_provider import LLMProvider
from config.settings import settings

class SparkAgent:
    """Agent for Spark optimization recommendations"""
    
    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize Spark Agent
        
        Args:
            llm_provider: LLM provider instance
        """
        self.llm = llm_provider
        self.system_prompt = settings.SPARK_AGENT_PROMPT
    
    def generate_optimization_tips(
        self,
        schema_context: str,
        query_context: str = ""
    ) -> Dict[str, Any]:
        """
        Generate Spark optimization recommendations
        
        Args:
            schema_context: Schema information
            query_context: Optional query or processing context
            
        Returns:
            Dictionary with optimization tips and code examples
        """
        prompt = f"""Analyze the following data schema and provide Spark optimization recommendations:

Schema:
{schema_context}

{f"Processing Context: {query_context}" if query_context else ""}

Provide optimization recommendations in the following areas:
1. Partitioning Strategy - How to partition the data for optimal performance
2. Caching Recommendations - When and what to cache
3. Join Optimization - Broadcast joins vs shuffle joins
4. Data Skew Handling - How to handle skewed data
5. File Format Recommendations - Parquet, ORC, etc.
6. Compression Settings - Best compression codecs
7. Memory Configuration - Executor and driver memory settings
8. Code Optimization - PySpark code best practices

For each recommendation, provide:
- Description
- PySpark code example (if applicable)
- Expected performance impact

Format your response with clear headers and code blocks.
"""
        
        try:
            response = self.llm.generate(prompt, system_message=self.system_prompt)
            
            # Extract code examples
            code_examples = self._extract_code_blocks(response)
            
            return {
                "optimization_tips": response,
                "code_examples": code_examples,
                "summary": self._generate_summary(response)
            }
        except Exception as e:
            return {
                "error": str(e),
                "optimization_tips": "",
                "code_examples": [],
                "summary": ""
            }
    
    def _extract_code_blocks(self, response: str) -> list:
        """Extract code blocks from response"""
        code_blocks = []
        
        # Find all code blocks
        start_markers = ["```python", "```pyspark", "```"]
        
        for marker in start_markers:
            pos = 0
            while marker in response[pos:]:
                start = response.find(marker, pos) + len(marker)
                end = response.find("```", start)
                if end != -1:
                    code = response[start:end].strip()
                    if code:
                        code_blocks.append(code)
                    pos = end + 3
                else:
                    break
        
        return code_blocks
    
    def _generate_summary(self, response: str) -> str:
        """Generate a summary of optimization tips"""
        # Count the number of recommendations
        headers = [
            "Partitioning",
            "Caching",
            "Join",
            "Skew",
            "Format",
            "Compression",
            "Memory",
            "Code"
        ]
        
        count = sum(1 for header in headers if header.lower() in response.lower())
        return f"Generated {count} categories of Spark optimization recommendations"
