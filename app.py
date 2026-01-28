"""
AI Data Engineer Assistant - Main Streamlit Application
"""
import streamlit as st
import os
from pathlib import Path

# Import core modules
from core import CSVReader, EmbeddingGenerator, VectorStore, LLMProvider
from agents import DataEngineerGraph
from ui import (
    get_custom_css,
    display_schema_info,
    display_sql_result,
    display_quality_result,
    display_spark_result,
    display_dependency_result,
    display_documentation_result
)
from config.settings import settings
from utils import setup_logging

# Setup logging
logger = setup_logging()

# Page configuration
st.set_page_config(
    page_title="AI Data Engineer Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state
if 'csv_reader' not in st.session_state:
    st.session_state.csv_reader = None
if 'schema_context' not in st.session_state:
    st.session_state.schema_context = ""
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'llm_provider' not in st.session_state:
    st.session_state.llm_provider = None
if 'agent_graph' not in st.session_state:
    st.session_state.agent_graph = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False

def initialize_components():
    """Initialize LLM and agent components"""
    try:
        if not st.session_state.llm_provider:
            with st.spinner("Initializing AI components..."):
                # Initialize LLM provider
                st.session_state.llm_provider = LLMProvider()
                
                # Initialize agent graph
                st.session_state.agent_graph = DataEngineerGraph(st.session_state.llm_provider)
                
                st.success("✅ AI components initialized successfully!")
                return True
    except Exception as e:
        st.error(f"❌ Error initializing components: {str(e)}")
        if "OPENAI_API_KEY" in str(e):
            st.warning("⚠️ Please set your OpenAI API key in the sidebar.")
        return False
    return True

def process_csv_file(uploaded_file):
    """Process uploaded CSV file"""
    try:
        with st.spinner("Processing CSV file..."):
            # Read CSV
            csv_reader = CSVReader()
            file_content = uploaded_file.read()
            df = csv_reader.read_csv(file_content, uploaded_file.name)
            
            # Store in session state
            st.session_state.csv_reader = csv_reader
            st.session_state.schema_context = csv_reader.get_schema_text()
            st.session_state.file_uploaded = True
            
            # Initialize embeddings and vector store
            embedding_gen = EmbeddingGenerator()
            vector_store = VectorStore()
            vector_store.create_collection(f"schema_{uploaded_file.name}")
            
            # Generate and store embeddings
            schema_text = csv_reader.get_schema_text()
            embedding = embedding_gen.generate_embedding(schema_text)
            
            vector_store.add_documents(
                documents=[schema_text],
                embeddings=[embedding.tolist()],
                metadatas=[{"filename": uploaded_file.name}]
            )
            
            st.session_state.vector_store = vector_store
            
            st.success(f"✅ Successfully processed {uploaded_file.name}!")
            
            # Display schema info
            display_schema_info(
                csv_reader.get_schema(),
                csv_reader.get_metadata()
            )
            
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        logger.error(f"Error processing CSV: {str(e)}")

def handle_question(question: str, agent_type: str = None):
    """Handle user question"""
    if not st.session_state.file_uploaded:
        st.warning("⚠️ Please upload a CSV file first!")
        return
    
    if not st.session_state.agent_graph:
        if not initialize_components():
            return
    
    try:
        with st.spinner("🤔 Thinking..."):
            # Run agent graph
            result = st.session_state.agent_graph.run(
                question=question,
                schema_context=st.session_state.schema_context,
                agent_type=agent_type
            )
            
            # Add to chat history
            st.session_state.chat_history.append({
                "question": question,
                "result": result,
                "agent_type": agent_type
            })
            
            # Display result based on agent type
            if agent_type == "sql" or any(kw in question.lower() for kw in ["sql", "query", "select"]):
                display_sql_result(result)
            elif agent_type == "quality" or any(kw in question.lower() for kw in ["quality", "validation"]):
                display_quality_result(result)
            elif agent_type == "spark" or any(kw in question.lower() for kw in ["spark", "optimization"]):
                display_spark_result(result)
            elif agent_type == "dependency" or any(kw in question.lower() for kw in ["dependency", "relationship"]):
                display_dependency_result(result)
            elif agent_type == "documentation" or any(kw in question.lower() for kw in ["documentation", "document"]):
                display_documentation_result(result)
            else:
                # Default display
                st.json(result)
                
    except Exception as e:
        st.error(f"❌ Error processing question: {str(e)}")
        logger.error(f"Error handling question: {str(e)}")

# Main UI
def main():
    """Main application"""
    
    # Header
    st.title("🤖 AI Data Engineer Assistant")
    st.markdown("*Powered by LangGraph, OpenAI, and Streamlit*")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Enter your OpenAI API key"
        )
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            settings.OPENAI_API_KEY = api_key
        
        st.divider()
        
        # File upload
        st.header("📁 Upload CSV")
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload a CSV file to analyze"
        )
        
        if uploaded_file and not st.session_state.file_uploaded:
            process_csv_file(uploaded_file)
        
        st.divider()
        
        # Agent selection
        st.header("🎯 Select Agent")
        agent_type = st.selectbox(
            "Choose an agent",
            ["Auto-detect", "SQL Generator", "Data Quality", "Spark Optimization", "Dependencies", "Documentation"],
            help="Select which agent to use (Auto-detect will choose based on your question)"
        )
        
        agent_type_map = {
            "Auto-detect": None,
            "SQL Generator": "sql",
            "Data Quality": "quality",
            "Spark Optimization": "spark",
            "Dependencies": "dependency",
            "Documentation": "documentation"
        }
        
        selected_agent = agent_type_map[agent_type]
        
        st.divider()
        
        # Info
        st.header("ℹ️ About")
        st.markdown("""
        This AI assistant helps data engineers with:
        - 🔍 SQL query generation
        - ✅ Data quality rules
        - ⚡ Spark optimization
        - 🔗 Table dependencies
        - 📚 Documentation
        """)
        
        # Reset button
        if st.button("🔄 Reset Session"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Main content area
    if not st.session_state.file_uploaded:
        st.info("👈 Please upload a CSV file from the sidebar to get started!")
        
        # Show example questions
        st.subheader("💡 Example Questions")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **SQL Generation:**
            - Generate a query to find top 10 customers
            - Write SQL to calculate monthly revenue
            
            **Data Quality:**
            - Suggest data quality rules for this dataset
            - What validation checks should I implement?
            """)
        
        with col2:
            st.markdown("""
            **Spark Optimization:**
            - How can I optimize this data processing?
            - Suggest partitioning strategy
            
            **Documentation:**
            - Generate a data dictionary
            - Create a README for this dataset
            """)
    else:
        # Question input
        st.subheader("💬 Ask a Question")
        
        # Quick action buttons
        st.markdown("**Quick Actions:**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Generate SQL"):
                handle_question("Generate SQL queries for common analysis tasks", "sql")
        
        with col2:
            if st.button("✅ Quality Rules"):
                handle_question("Generate data quality rules", "quality")
        
        with col3:
            if st.button("⚡ Optimize Spark"):
                handle_question("Suggest Spark optimization strategies", "spark")
        
        with col4:
            if st.button("📚 Documentation"):
                handle_question("Generate data dictionary", "documentation")
        
        st.divider()
        
        # Custom question input
        question = st.text_area(
            "Or ask your own question:",
            placeholder="e.g., Generate a SQL query to find customers with orders > $1000",
            height=100
        )
        
        if st.button("🚀 Submit Question", type="primary"):
            if question:
                handle_question(question, selected_agent)
            else:
                st.warning("⚠️ Please enter a question!")
        
        # Display chat history
        if st.session_state.chat_history:
            st.divider()
            st.subheader("📜 Chat History")
            
            for idx, chat in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"Q{len(st.session_state.chat_history) - idx}: {chat['question'][:50]}..."):
                    st.markdown(f"**Question:** {chat['question']}")
                    st.markdown(f"**Agent:** {chat.get('agent_type', 'auto')}")
                    
                    # Display result based on type
                    result = chat['result']
                    if 'sql_query' in result:
                        display_sql_result(result)
                    elif 'quality_rules' in result:
                        display_quality_result(result)
                    elif 'optimization_tips' in result:
                        display_spark_result(result)
                    elif 'dependency_analysis' in result:
                        display_dependency_result(result)
                    elif 'documentation' in result:
                        display_documentation_result(result)

if __name__ == "__main__":
    main()
