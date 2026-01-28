# Quick Start Guide

## ✅ Setup Complete!

All dependencies have been installed successfully. You're ready to run the AI Data Engineer Assistant!

## 🚀 Running the Application

### Step 1: Set Your OpenAI API Key

Edit the `.env` file and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_actual_api_key_here
```

Or you can enter it directly in the Streamlit sidebar when the app runs.

### Step 2: Start the Application

Run this command in your terminal:

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

### Step 3: Upload a CSV File

1. Click "Browse files" in the sidebar
2. Upload a CSV file (or use `sample_data/example.csv` for testing)
3. The app will automatically extract the schema and display statistics

### Step 4: Ask Questions

Use the quick action buttons or type your own questions:

**Example Questions:**
- "Generate a query to find top 10 customers by revenue"
- "Suggest data quality rules for this dataset"
- "How can I optimize Spark processing for this data?"
- "Analyze table relationships"
- "Generate a data dictionary"

## 📝 Features

- **SQL Generation**: Natural language to SQL queries
- **Data Quality**: Automated quality rule suggestions
- **Spark Optimization**: Performance tuning recommendations
- **Dependencies**: Table relationship analysis
- **Documentation**: Auto-generate data dictionaries and docs

## 🔧 Troubleshooting

### If you see "No module named 'langchain_openai'"
Run: `pip install langchain-openai langchain-community langgraph`

### If you see API key errors
Make sure your OpenAI API key is set in the `.env` file or entered in the sidebar

### If the app doesn't start
Make sure you're in the correct directory:
```bash
cd C:\Users\Lokesh_Gupta\.gemini\antigravity\scratch\ai-data-engineer-assistant
```

## 🎯 Next Steps

1. **Test with Sample Data**: Use `sample_data/example.csv`
2. **Try All Agents**: Test SQL, Quality, Spark, Dependencies, and Documentation
3. **Export Results**: Download generated SQL, rules, and docs
4. **Switch to Llama 3**: Follow instructions in README.md to use local LLMs

## 📚 Documentation

- Full documentation: `README.md`
- Implementation details: See walkthrough artifact
- Configuration: `config/settings.py`

---

**Ready to go! Run `streamlit run app.py` to start!** 🚀
