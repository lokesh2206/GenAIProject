"""
LangGraph Workflow - Orchestrates multiple agents
"""
from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain.schema import HumanMessage
import operator

from .sql_agent import SQLAgent
from .quality_agent import QualityAgent
from .spark_agent import SparkAgent
from .dependency_agent import DependencyAgent
from .documentation_agent import DocumentationAgent
from core.llm_provider import LLMProvider

class AgentState(TypedDict):
    """State for the agent graph"""
    question: str
    schema_context: str
    agent_type: str
    result: Dict[str, Any]
    messages: Annotated[list, operator.add]

class DataEngineerGraph:
    """LangGraph workflow for data engineer assistant"""
    
    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize the graph
        
        Args:
            llm_provider: LLM provider instance
        """
        self.llm = llm_provider
        
        # Initialize agents
        self.sql_agent = SQLAgent(llm_provider)
        self.quality_agent = QualityAgent(llm_provider)
        self.spark_agent = SparkAgent(llm_provider)
        self.dependency_agent = DependencyAgent(llm_provider)
        self.documentation_agent = DocumentationAgent(llm_provider)
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent
        workflow.add_node("sql_agent", self._sql_node)
        workflow.add_node("quality_agent", self._quality_node)
        workflow.add_node("spark_agent", self._spark_node)
        workflow.add_node("dependency_agent", self._dependency_node)
        workflow.add_node("documentation_agent", self._documentation_node)
        
        # Set entry point with conditional routing
        workflow.set_conditional_entry_point(
            self._route_question,
            {
                "sql": "sql_agent",
                "quality": "quality_agent",
                "spark": "spark_agent",
                "dependency": "dependency_agent",
                "documentation": "documentation_agent"
            }
        )
        
        # All nodes end after execution
        workflow.add_edge("sql_agent", END)
        workflow.add_edge("quality_agent", END)
        workflow.add_edge("spark_agent", END)
        workflow.add_edge("dependency_agent", END)
        workflow.add_edge("documentation_agent", END)
        
        return workflow.compile()
    
    def _route_question(self, state: AgentState) -> str:
        """Route question to appropriate agent"""
        question = state["question"].lower()
        
        # Check for explicit agent type
        if state.get("agent_type"):
            return state["agent_type"]
        
        # Route based on keywords
        if any(keyword in question for keyword in ["sql", "query", "select", "join", "where"]):
            return "sql"
        elif any(keyword in question for keyword in ["quality", "validation", "check", "rule"]):
            return "quality"
        elif any(keyword in question for keyword in ["spark", "optimization", "performance", "partition"]):
            return "spark"
        elif any(keyword in question for keyword in ["dependency", "relationship", "foreign key", "lineage"]):
            return "dependency"
        elif any(keyword in question for keyword in ["documentation", "document", "readme", "dictionary"]):
            return "documentation"
        else:
            # Default to SQL for general questions
            return "sql"
    
    def _sql_node(self, state: AgentState) -> Dict[str, Any]:
        """SQL agent node"""
        result = self.sql_agent.generate_sql(
            state["question"],
            state["schema_context"]
        )
        return {
            "result": result,
            "messages": [HumanMessage(content=f"SQL Agent: {result.get('sql_query', 'No query generated')}")]
        }
    
    def _quality_node(self, state: AgentState) -> Dict[str, Any]:
        """Quality agent node"""
        result = self.quality_agent.generate_quality_rules(
            state["schema_context"]
        )
        return {
            "result": result,
            "messages": [HumanMessage(content=f"Quality Agent: Generated quality rules")]
        }
    
    def _spark_node(self, state: AgentState) -> Dict[str, Any]:
        """Spark agent node"""
        result = self.spark_agent.generate_optimization_tips(
            state["schema_context"],
            state.get("question", "")
        )
        return {
            "result": result,
            "messages": [HumanMessage(content=f"Spark Agent: Generated optimization tips")]
        }
    
    def _dependency_node(self, state: AgentState) -> Dict[str, Any]:
        """Dependency agent node"""
        result = self.dependency_agent.analyze_dependencies(
            state["schema_context"]
        )
        return {
            "result": result,
            "messages": [HumanMessage(content=f"Dependency Agent: Analyzed dependencies")]
        }
    
    def _documentation_node(self, state: AgentState) -> Dict[str, Any]:
        """Documentation agent node"""
        # Determine doc type from question
        doc_type = "data_dictionary"
        if "readme" in state["question"].lower():
            doc_type = "readme"
        elif "schema" in state["question"].lower():
            doc_type = "schema_doc"
        
        result = self.documentation_agent.generate_documentation(
            state["schema_context"],
            doc_type
        )
        return {
            "result": result,
            "messages": [HumanMessage(content=f"Documentation Agent: Generated {doc_type}")]
        }
    
    def run(self, question: str, schema_context: str, agent_type: str = None) -> Dict[str, Any]:
        """
        Run the graph with a question
        
        Args:
            question: User's question
            schema_context: Schema information
            agent_type: Optional explicit agent type
            
        Returns:
            Result from the appropriate agent
        """
        initial_state = {
            "question": question,
            "schema_context": schema_context,
            "agent_type": agent_type,
            "result": {},
            "messages": []
        }
        
        final_state = self.graph.invoke(initial_state)
        return final_state.get("result", {})
