import streamlit as st
import PyPDF2
from docx import Document
from transformers import pipeline

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

# Function to extract text from a DOCX (Word) file
def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to extract text from a TXT file
def extract_text_from_txt(txt_file):
    text = txt_file.read().decode('utf-8')
    return text

# Function to determine the file type and extract text accordingly
def extract_text_from_file(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith('.docx'):
        return extract_text_from_docx(uploaded_file)
    elif uploaded_file.name.endswith('.txt'):
        return extract_text_from_txt(uploaded_file)
    else:
        raise ValueError("Unsupported file format. Please upload a .pdf, .docx, or .txt file.")

# Load the pre-trained question-answering model (RoBERTa in this case)
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

# Function to get the answer from the document text based on the query
def get_answer_from_text(query, context):
    result = qa_pipeline(question=query, context=context)
    return result['answer']

# Streamlit App
st.title("Document-based Question Answering System")

# File uploader
uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    try:
        # Extract text from the uploaded file
        document_text = extract_text_from_file(uploaded_file)
        st.write("Document text extracted successfully.")
    except ValueError as e:
        st.error(e)

    # Query input
    query = st.text_input("Enter your query:")

    if st.button("Get Answer"):
        if query and document_text:
            # Get the answer from the text based on the query
            answer = get_answer_from_text(query, document_text)
            st.write(f"Answer: {answer}")
        else:
            st.write("Please provide a query and upload a valid document.")

