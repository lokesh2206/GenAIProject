"""
SQL Generation Agent
"""
from typing import Dict, Any
from core.llm_provider import LLMProvider
from config.settings import settings

class SQLAgent:
    """Agent for generating SQL queries"""
    
    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize SQL Agent
        
        Args:
            llm_provider: LLM provider instance
        """
        self.llm = llm_provider
        self.system_prompt = settings.SQL_AGENT_PROMPT
    
    def generate_sql(self, question: str, schema_context: str) -> Dict[str, Any]:
        """
        Generate SQL query based on question and schema
        
        Args:
            question: User's question
            schema_context: Schema information
            
        Returns:
            Dictionary with SQL query and explanation
        """
        prompt = f"""Given the following database schema:

{schema_context}

User Question: {question}

Generate a SQL query to answer this question. Provide:
1. The SQL query with proper formatting
2. A brief explanation of what the query does
3. Any assumptions made

Format your response as:
SQL Query:
```sql
[your query here]
```

Explanation:
[your explanation here]

Assumptions:
[any assumptions made]
"""
        
        try:
            response = self.llm.generate(prompt, system_message=self.system_prompt)
            
            # Parse the response
            sql_query = self._extract_sql(response)
            explanation = self._extract_section(response, "Explanation:")
            assumptions = self._extract_section(response, "Assumptions:")
            
            return {
                "sql_query": sql_query,
                "explanation": explanation,
                "assumptions": assumptions,
                "full_response": response
            }
        except Exception as e:
            return {
                "error": str(e),
                "sql_query": "",
                "explanation": "",
                "assumptions": ""
            }
    
    def _extract_sql(self, response: str) -> str:
        """Extract SQL query from response"""
        try:
            # Look for SQL code block
            if "```sql" in response:
                start = response.find("```sql") + 6
                end = response.find("```", start)
                return response[start:end].strip()
            elif "```" in response:
                start = response.find("```") + 3
                end = response.find("```", start)
                return response[start:end].strip()
            else:
                # Try to find SQL Query: section
                if "SQL Query:" in response:
                    start = response.find("SQL Query:") + 10
                    end = response.find("\n\n", start)
                    return response[start:end].strip()
                return response.strip()
        except:
            return response.strip()
    
    def _extract_section(self, response: str, section_name: str) -> str:
        """Extract a section from the response"""
        try:
            if section_name in response:
                start = response.find(section_name) + len(section_name)
                # Find the next section or end
                next_sections = ["SQL Query:", "Explanation:", "Assumptions:"]
                end = len(response)
                for next_section in next_sections:
                    if next_section != section_name and next_section in response[start:]:
                        potential_end = response.find(next_section, start)
                        if potential_end < end:
                            end = potential_end
                return response[start:end].strip()
            return ""
        except:
            return ""
