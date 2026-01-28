# AI Data Engineer Assistant

An intelligent assistant powered by LangGraph and GenAI that helps data engineers analyze CSV files, generate SQL queries, create data quality rules, optimize Spark jobs, analyze table dependencies, and generate documentation.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)

## Features

- **CSV Analysis**: Upload and analyze CSV files with automatic schema extraction
- **SQL Generation**: Generate SQL queries from natural language questions
- **Data Quality Rules**: Automatically suggest comprehensive data quality validation rules
- **Spark Optimization**: Get PySpark optimization recommendations and best practices
- **Dependency Analysis**: Identify table relationships and data lineage
- **Documentation**: Generate data dictionaries, READMEs, and schema documentation

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **LLM** | OpenAI GPT (switchable to Llama 3/Mistral via Ollama) |
| **Agents** | LangGraph |
| **Embeddings** | SentenceTransformers |
| **Vector DB** | ChromaDB |
| **UI** | Streamlit |
| **Backend** | Python |

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (or Ollama for local LLMs)
- pip package manager

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-data-engineer-assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   # OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Running Locally

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

3. **Upload a CSV file**
   - Click "Browse files" in the sidebar
   - Select your CSV file

4. **Ask questions**
   - Use quick action buttons or type custom questions
   - The AI will automatically route to the appropriate agent

### Example Questions

**SQL Generation:**
- "Generate a query to find top 10 customers by revenue"
- "Write SQL to calculate monthly sales trends"

**Data Quality:**
- "Suggest data quality rules for this dataset"
- "What validation checks should I implement?"

**Spark Optimization:**
- "How can I optimize processing for this data?"
- "Suggest a partitioning strategy"

**Dependencies:**
- "Analyze table relationships"
- "Show potential foreign key relationships"

**Documentation:**
- "Generate a data dictionary"
- "Create a README for this dataset"

### Customizing Agent Prompts

Edit `config/settings.py` to customize system prompts for each agent.

## Project Structure

```
ai-data-engineer-assistant/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── config/
│   └── settings.py            # Configuration management
├── agents/
│   ├── graph.py               # LangGraph workflow
│   ├── sql_agent.py           # SQL generation
│   ├── quality_agent.py       # Data quality rules
│   ├── spark_agent.py         # Spark optimization
│   ├── dependency_agent.py    # Table dependencies
│   └── documentation_agent.py # Documentation generation
├── core/
│   ├── csv_reader.py          # CSV processing
│   ├── embeddings.py          # SentenceTransformers
│   ├── vector_store.py        # ChromaDB integration
│   └── llm_provider.py        # LLM abstraction
├── ui/
│   ├── components.py          # Reusable UI components
│   └── styles.py              # Custom CSS
├── utils/
│   └── helpers.py             # Utility functions
└── sample_data/
    └── example.csv            # Sample dataset
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.


