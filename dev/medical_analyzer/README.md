# Medical Document Analyzer

A comprehensive system for analyzing medical documents, extracting key information, and providing validation of diagnoses using AI. This project combines document processing, large language models, and structured workflows to transform medical PDFs into actionable insights.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Setup Instructions](#setup-instructions)
4. [Directory Structure](#directory-structure)
5. [How It Works](#how-it-works)
6. [Usage Guide](#usage-guide)
7. [API Reference](#api-reference)
8. [Customization](#customization)
9. [Troubleshooting](#troubleshooting)

## Project Overview

Medical Document Analyzer is a web-based application that processes medical PDFs to extract, analyze, and validate medical information. It uses cutting-edge AI techniques to:

- Extract text from medical PDFs
- Analyze medical conditions, symptoms, and treatments
- Generate concise medical summaries
- Validate diagnoses against symptoms
- Suggest treatment alternatives or improvements
- Present findings in a user-friendly web interface

The project combines LangGraph (for orchestrating AI workflows), language models from Groq and Mistral, and FastAPI for the web interface.

## Features

- **PDF Processing**: Extract text from PDF medical documents
- **AI Analysis**: In-depth analysis of medical conditions, treatments, and diagnoses
- **Summary Generation**: Concise, structured medical summaries
- **Diagnosis Validation**: AI-powered verification of diagnosis accuracy
- **Interactive Web UI**: User-friendly interface with Markdown rendering
- **Workflow Visualization**: Graph visualization of the analysis process
- **Light/Dark Theme**: Toggle between display modes for comfort

## Setup Instructions

### Prerequisites

- Python 3.10+ installed
- Basic knowledge of terminal/command line
- Internet connection for downloading dependencies

### Installation Steps

1. **Clone the repository (or download and extract)**

   ```bash
   git clone https://github.com/yourusername/medical-document-analyzer.git
   cd medical-document-analyzer
   ```

2. **Create and activate a virtual environment**

   For Windows:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   For Mac/Linux:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a .env file for API keys**

   Create a file named `.env` in the project root with the following content:

   ```
   MISTRAL_API_KEY=your_mistral_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

   You can obtain these API keys from:

   - Mistral AI: [https://console.mistral.ai/](https://console.mistral.ai/)
   - Groq: [https://console.groq.com/](https://console.groq.com/)

5. **Create required directories**

   ```bash
   mkdir -p static data templates
   ```

6. **Add a simple loading icon to static directory**

   Create or download a loading.gif file and place it in the `static` directory.

### Running the Application

1. **Start the FastAPI server**

   ```bash
   cd dev/medical_analyzer
   uvicorn api:app --reload
   ```

2. **Access the web interface**

   Open your browser and go to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Directory Structure

```
medical_analyzer/
├── api.py                # FastAPI web server implementation
├── main.py               # Core medical analysis logic
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── static/               # Static files (CSS, JS, images)
│   └── loading.gif       # Loading animation
├── templates/            # HTML templates
│   └── index.html        # Main web interface
└── data/                 # Storage for uploaded documents
```

## How It Works

### Technical Architecture

The system follows these key steps:

1. **Document Upload**: Medical PDF is uploaded through FastAPI
2. **Text Extraction**: Mistral API extracts text from the PDF
3. **Analysis Workflow**: LangGraph orchestrates the analysis:
   - **Context Extraction**: Pulls key information from the document
   - **Document Analysis**: AI analyzes medical contents
   - **Summary Generation**: Creates a structured summary
   - **Validation**: Checks diagnosis against symptoms and treatments
4. **Result Presentation**: Findings displayed in the web UI

### AI Components

- **Text Extraction**: Mistral OCR API
- **Medical Analysis**: DeepSeek-R1-Distill-Llama-70B via Groq
- **Summary Generation**: Mixtral-8x7b-32768 via Groq
- **Workflow Orchestration**: LangGraph for managing state transitions

## Usage Guide

### Analyzing a Medical Document

1. **Open the application** at [http://127.0.0.1:8000](http://127.0.0.1:8000)
2. **Click "Get Started"** to navigate to the upload section
3. **Select a PDF file** containing medical information
   - Patient records
   - Medical reports
   - Clinical notes
4. **Click "Analyze Document"** and wait for processing
5. **Review Results**: The analysis displays in three sections:
   - **Document Analysis**: Detailed analysis of medical information
   - **Medical Summary**: Structured overview of key findings
   - **Diagnosis Validation**: Assessment of diagnosis accuracy

### Example Documents

For testing, you can use synthetic medical reports. A sample is included in the repository (`synthetic_medical_report.pdf`). If not available, you can create one using any medical report template.

## API Reference

The system offers several API endpoints:

- **GET `/`**: Main web interface
- **POST `/analyze-medical-document`**: Upload and analyze a PDF document
- **DELETE `/cleanup`**: Remove PDF files older than 24 hours

### Command-line Usage

You can also use the system from the command line:

```bash
python main.py path/to/document.pdf --output results.txt
```

## Customization

### Using Different Models

Edit `main.py` to change the AI models:

```python
# Change Groq models
summary_llm = ChatGroq(
    model="your-preferred-model",
    temperature=0,
)
analyzer_llm = ChatGroq(
    model="your-preferred-model",
    temperature=0.6
)
```

### Modifying Analysis Steps

The workflow is defined in `create_medical_analysis_chain()`. You can add or modify steps by adjusting the state graph:

```python
# Add a new node
workflow.add_node("new_step", new_step_function)
# Update the graph edges
workflow.add_edge("previous_step", "new_step")
workflow.add_edge("new_step", "next_step")
```

## Troubleshooting

### Common Issues

1. **API Key Errors**

   - Ensure your `.env` file contains valid API keys
   - Check that `python-dotenv` is installed
   - Verify the API keys have appropriate permissions

2. **PDF Processing Errors**

   - Ensure the PDF is not password-protected
   - Check PDF is readable and not corrupted
   - Verify Mistral OCR API is accessible

3. **Web Interface Not Loading**
   - Check that FastAPI is running (`uvicorn api:app --reload`)
   - Verify the templates directory contains `index.html`
   - Ensure static files are properly mounted

### Getting Help

If you encounter problems not covered here:

1. Check the console output for error messages
2. Verify all dependencies are installed correctly
3. Ensure API keys are valid and have sufficient credits
4. Check network connectivity for API access

---

## Contributing

Contributions to improve the Medical Document Analyzer are welcome! Feel free to:

- Report bugs
- Suggest enhancements
- Submit pull requests
- Improve documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

_This project is for educational purposes only and should not be used for real medical diagnosis or treatment decisions._
