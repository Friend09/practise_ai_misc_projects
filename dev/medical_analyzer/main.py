# main.py

from typing import Dict, Any
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from pathlib import Path
import base64
from io import BytesIO
from mistralai import Mistral
from typing_extensions import TypedDict
import os
from dotenv import load_dotenv
import argparse

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# initialize clients
summary_llm = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
)
analyzer_llm = ChatGroq(model="DeepSeek-R1-Distill-Llama-70B", temperature=0.6)


def extract_pdf(pdf_name):
    # Upload the PDF file to the Mistral client for OCR processing
    uploaded_pdf = client.files.upload(
        file={
            "file_name": pdf_name,  # Specify the file name
            "content": open(pdf_name, "rb"),  # Open the file in binary mode
        },
        purpose="ocr",  # Specify the purpose as OCR
    )

    # Get a signed URL for the uploaded file
    # Fix: Use dot notation instead of dictionary access
    signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)

    # Process the uploaded document using the OCR model
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",  # Specify the OCR model to use
        document={
            "type": "document_url",  # Indicate the document type as a URL
            "document_url": signed_url.url,  # Provide the signed URL of the document
        },
    )

    # Extract and combine the text content from all pages of the OCR response
    text = "\n\n".join([page.markdown for page in ocr_response.pages])

    # Return the extracted text
    return text


# == Langgraph ==
class MedicalAnalysisState(TypedDict):
    file_name: str
    context: str
    analysis_result: str
    summary: str
    validation_result: str  # Changed from validation_results to validation_result


def create_medical_analysis_chain():
    # define the nodes (agents) in our graph
    def extract_context(state: MedicalAnalysisState):
        print("----------------------------------------------------")
        print("-----------Extracting context from PDF--------------")
        print("----------------------------------------------------")
        pdf_name = state["file_name"]
        text = extract_pdf(pdf_name)
        state["context"] = text
        return state

    def analyze_document(state: MedicalAnalysisState):
        print("----------------------------------------------------")
        print("------------Analyzing context from PDF--------------")
        print("----------------------------------------------------")
        messages = state["context"]
        document_content = messages

        # langchain groq for medical analysis
        messages = [
            SystemMessage(
                content="""You are a medical document analyzer. Extract key information and format it in markdown with the following sections:

                ### Date of Incident
                - Specify the date when the medical incident occurred

                ### Medical Facility
                - Name of the medical center/hospital
                - Location details

                ### Healthcare Providers
                - Primary physician
                - Other medical staff involved

                ### Patient Information
                - Chief complaints
                - Vital signs
                - Relevant medical history

                ### Medications
                - Current medications
                - New prescriptions
                - Dosage information

                Please ensure the response is well-formatted in markdown with appropriate headers and bullet points."""
            ),
            HumanMessage(content=document_content),
        ]
        response = analyzer_llm.invoke(messages)
        state["analysis_result"] = response.content.split("</think>")[-1]
        return state

    def generate_summary(state: MedicalAnalysisState):
        print("----------------------------------------------------")
        print("------------Generating summary from PDF-------------")
        print("----------------------------------------------------")
        analysis_result = state["analysis_result"]

        messages = [
            SystemMessage(
                content="""You are a medical report summarizer. Create a detailed summary in markdown format with the following sections:

                ### Key Findings
                - Main medical issues identified
                - Critical observations

                ### Diagnosis
                - Primary diagnosis
                - Secondary conditions (if any)

                ### Treatment Plan
                - Recommended procedures
                - Medications prescribed
                - Follow-up instructions

                ### Additional Notes
                - Important considerations
                - Special instructions

                Please ensure proper markdown formatting with headers, bullet points, and emphasis where appropriate."""
            ),
            HumanMessage(
                content=f"Generate a detailed medical summary report based on this analysis: {analysis_result}"
            ),
        ]
        response = summary_llm.invoke(messages)

        state["summary"] = response.content
        return state

    def validate_diagnosis(state: MedicalAnalysisState):
        print("----------------------------------------------------")
        print("------------Validating diagnosis from PDF-----------")
        print("----------------------------------------------------")
        analysis_result = state["analysis_result"]
        summary = state["summary"]

        messages = [
            SystemMessage(
                content="""You are a medical diagnosis validator. Provide your assessment in markdown format with these sections:

                ### Alignment Analysis
                - Evaluate if diagnosis matches symptoms
                - Assess treatment appropriateness
                - Review medication selections

                ### Recommendations
                - Alternative treatments to consider
                - Suggested medication adjustments
                - Additional tests if needed

                ### Risk Assessment
                - Potential complications
                - Drug interaction concerns
                - Follow-up recommendations

                Please format your response in clear markdown with appropriate headers and bullet points."""
            ),
            HumanMessage(
                content=f"""Analysis: {analysis_result}\nSummary: {summary}
                            Based on the Analysis and Summary provided please provide whether diagnosis,treatment and medication provided is in alignment with medical complaint.
                            If not in alignment then specify what best treatment and medication could have been provided.
                            """
            ),
        ]
        response = analyzer_llm.invoke(messages)

        state["validation_result"] = response.content.split("</think>")[-1]
        return state


    # create the graph
    workflow = StateGraph(MedicalAnalysisState)

    # add nodes
    workflow.add_node("extractor", extract_context)
    workflow.add_node("analyzer", analyze_document)
    workflow.add_node("summarizer", generate_summary)
    workflow.add_node("validator", validate_diagnosis)

    # define edges
    workflow.add_edge(START, "extractor")
    workflow.add_edge("extractor", "analyzer")
    workflow.add_edge("analyzer", "summarizer")
    workflow.add_edge("summarizer", "validator")
    workflow.add_edge("validator", END)

    # compile the graph
    chain = workflow.compile()

    # generate graph vizualization
    graph_png = chain.get_graph().draw_mermaid_png()
    graph_base64 = base64.b64encode(graph_png).decode('utf-8')

    return chain, graph_base64

def process_medical_document(document_path: str) -> Dict[str, Any]:

    # create the chain and get graph visualization
    chain, graph_viz = create_medical_analysis_chain()
    print(f"Document Path: {document_path}")

    # Process the document
    result = chain.invoke({"file_name": document_path})

    return {
        "analysis": result["analysis_result"],
        "summary": result["summary"],
        "validation": result["validation_result"],
        "graph": graph_viz,
    }


if __name__ == "__main__":

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process a medical document.")
    parser.add_argument(
        "document_path", type=str, help="Path to the medical document (PDF) to analyze."
    )
    parser.add_argument(
        "--output", "-o", type=str, help="Path to save the output results (optional)."
    )

    # Parse arguments
    args = parser.parse_args()

    # Process the document
    try:
        results = process_medical_document(args.document_path)

        # Format the output
        output_text = f"Analysis Result:\n{results['analysis']}\n\nSummary:\n{results['summary']}\n\nValidation:\n{results['validation']}"

        # Print to console
        print(output_text)

        # Save to file if output path is specified
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_text)
            print(f"\nResults saved to {args.output}")

    except Exception as e:
        print(f"An error occurred: {e}")
