"""
Custom CSS styles for the Streamlit app
"""

def get_custom_css() -> str:
    """Get custom CSS for the app"""
    return """
    <style>
    /* Main container */
    .main {
        padding: 1rem 2rem;
        max-width: 1400px;
    }
    
    /* Block container spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Headers */
    h1 {
        color: #1f77b4;
        font-weight: 700;
        margin-bottom: 1.5rem;
        margin-top: 0;
    }
    
    h2 {
        color: #2c3e50;
        font-weight: 600;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        clear: both;
    }
    
    h3 {
        color: #34495e;
        font-weight: 500;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Spacing between sections */
    div[data-testid="stVerticalBlock"] > div {
        margin-bottom: 1rem;
    }
    
    /* Button container spacing */
    div[data-testid="column"] {
        padding: 0.25rem;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        margin-top: 1rem;
        display: flex;
        flex-direction: column;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #1f77b4;
    }
    
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background-color: #282c34;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Buttons */
    .stButton {
        margin-bottom: 0.5rem;
    }
    
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 0.5rem;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
        margin: 0.25rem 0;
    }
    
    .stButton > button:hover {
        background-color: #1565c0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transform: translateY(-1px);
    }
    
    /* Text area and input spacing */
    .stTextArea, .stTextInput {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Divider spacing */
    hr {
        margin: 2rem 0;
    }
    
    /* File uploader */
    .uploadedFile {
        border: 2px dashed #1f77b4;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        padding: 2rem 1rem;
    }
    
    /* Success/Info boxes */
    .stSuccess {
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .stInfo {
        background-color: #d1ecf1;
        border-color: #bee5eb;
        color: #0c5460;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Metrics */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-weight: 500;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        font-weight: 500;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
    }
    
    .streamlit-expanderContent {
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background-color: #4caf50;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        border: none;
        margin-top: 1rem;
    }
    
    .stDownloadButton > button:hover {
        background-color: #45a049;
    }
    
    /* Markdown content spacing */
    .stMarkdown {
        margin: 0.5rem 0;
    }
    
    /* Prevent text overflow */
    .stMarkdown p, .stMarkdown li {
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    /* Column spacing */
    div[data-testid="column"] > div {
        padding: 0.5rem;
    }
    </style>
    """
