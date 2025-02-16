# AI Practice Projects

Collection of practice projects exploring various AI/ML techniques and tools.

## Projects

### 1. RAG Context Relevancy Checker

Implementation of a RAG (Retrieval Augmented Generation) system that evaluates context relevancy for question answering using:

- LangChain with Groq and HuggingFace models
- Vector store using ChromaDB
- PDF document processing
- Semantic chunking and embeddings

### 2. Text-to-SQL Agent

Interactive SQL query generator using:

- LangChain with OpenAI
- SQLite database integration
- Step-by-step reasoning approach
- Graph-based agent architecture

## Setup

1. Install dependencies:

   ```sh
   make install
   ```

2. Create a `.env` file with required API keys, set environment variables:

   ```sh
   OPENAI_API_KEY=<your-key>
   GROQ_API_KEY=<your-key>
   HF_TOKEN=<your-key>
   ```

## Project Structure

```
.
├── data/               # Data files and vector stores
├── dev/                # Development scripts
├── notebooks/          # Jupyter notebooks
└── requirements.txt    # Project dependencies
```

## Key Dependencies

- `langchain` & related packages
- `chromadb`
- `transformers`
- `torch`
- `pdfplumber`
- `sqlalchemy`

## Usage

See individual notebook files for detailed usage examples:

- `RAG_Context_Relevancy_Checker.ipynb`
- `practise_text2sql_react.ipynb`
- more... WIP

## References

- RAG Context Relevancy Checker
- Implementing Reasoning in Text-to-SQL Agents
