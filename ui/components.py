"""
Reusable UI components
"""
import streamlit as st
from typing import Dict, Any

def display_schema_info(schema: Dict[str, Any], metadata: Dict[str, Any]):
    """
    Display schema information
    
    Args:
        schema: Schema dictionary
        metadata: Metadata dictionary
    """
    st.subheader("📊 Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Rows", f"{metadata.get('total_rows', 0):,}")
    
    with col2:
        st.metric("Total Columns", metadata.get('total_columns', 0))
    
    with col3:
        memory_mb = metadata.get('memory_usage_mb', 0)
        st.metric("Memory Usage", f"{memory_mb:.2f} MB")
    
    with col4:
        duplicates = metadata.get('duplicate_count', 0)
        st.metric("Duplicates", duplicates)
    
    # Display column details
    st.subheader("📋 Column Details")
    
    columns_data = schema.get('columns', [])
    if columns_data:
        for col_info in columns_data:
            with st.expander(f"**{col_info['column_name']}** ({col_info['inferred_type']})"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.write(f"**Data Type:** {col_info['data_type']}")
                    st.write(f"**Non-Null Count:** {col_info['non_null_count']}")
                    st.write(f"**Null Count:** {col_info['null_count']}")
                
                with col_b:
                    st.write(f"**Unique Values:** {col_info['unique_count']}")
                    if col_info.get('sample_values'):
                        st.write(f"**Sample Values:** {', '.join(map(str, col_info['sample_values'][:3]))}")
                
                # Show statistics for numeric columns
                if 'min' in col_info:
                    st.write(f"**Range:** {col_info['min']} to {col_info['max']}")
                    st.write(f"**Mean:** {col_info['mean']:.2f} | **Median:** {col_info['median']:.2f}")

def display_chat_message(role: str, content: str):
    """
    Display a chat message
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
    """
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 Assistant:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)

def display_sql_result(result: Dict[str, Any]):
    """Display SQL generation result"""
    if result.get('error'):
        st.error(f"Error: {result['error']}")
        return
    
    st.subheader("🔍 Generated SQL Query")
    
    sql_query = result.get('sql_query', '')
    if sql_query:
        st.code(sql_query, language='sql')
        
        # Download button
        st.download_button(
            label="📥 Download SQL",
            data=sql_query,
            file_name="generated_query.sql",
            mime="text/plain"
        )
    
    if result.get('explanation'):
        st.subheader("📝 Explanation")
        st.write(result['explanation'])
    
    if result.get('assumptions'):
        with st.expander("⚠️ Assumptions"):
            st.write(result['assumptions'])

def display_quality_result(result: Dict[str, Any]):
    """Display data quality rules result"""
    if result.get('error'):
        st.error(f"Error: {result['error']}")
        return
    
    st.subheader("✅ Data Quality Rules")
    
    full_response = result.get('full_response', '')
    if full_response:
        st.markdown(full_response)
        
        # Download button
        st.download_button(
            label="📥 Download Quality Rules",
            data=full_response,
            file_name="data_quality_rules.md",
            mime="text/markdown"
        )

def display_spark_result(result: Dict[str, Any]):
    """Display Spark optimization result"""
    if result.get('error'):
        st.error(f"Error: {result['error']}")
        return
    
    st.subheader("⚡ Spark Optimization Tips")
    
    optimization_tips = result.get('optimization_tips', '')
    if optimization_tips:
        st.markdown(optimization_tips)
        
        # Download button
        st.download_button(
            label="📥 Download Optimization Tips",
            data=optimization_tips,
            file_name="spark_optimization.md",
            mime="text/markdown"
        )

def display_dependency_result(result: Dict[str, Any]):
    """Display dependency analysis result"""
    if result.get('error'):
        st.error(f"Error: {result['error']}")
        return
    
    st.subheader("🔗 Table Dependencies")
    
    # Display mermaid diagram if available
    mermaid_diagram = result.get('mermaid_diagram', '')
    if mermaid_diagram:
        st.subheader("📊 Dependency Graph")
        st.code(mermaid_diagram, language='mermaid')
    
    dependency_analysis = result.get('dependency_analysis', '')
    if dependency_analysis:
        st.markdown(dependency_analysis)
        
        # Download button
        st.download_button(
            label="📥 Download Dependency Analysis",
            data=dependency_analysis,
            file_name="table_dependencies.md",
            mime="text/markdown"
        )

def display_documentation_result(result: Dict[str, Any]):
    """Display documentation result"""
    if result.get('error'):
        st.error(f"Error: {result['error']}")
        return
    
    doc_type = result.get('doc_type', 'documentation')
    st.subheader(f"📚 {doc_type.replace('_', ' ').title()}")
    
    documentation = result.get('documentation', '')
    if documentation:
        st.markdown(documentation)
        
        # Download button
        file_name = f"{doc_type}.md"
        st.download_button(
            label=f"📥 Download {doc_type.replace('_', ' ').title()}",
            data=documentation,
            file_name=file_name,
            mime="text/markdown"
        )
