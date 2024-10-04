import PyPDF2
from docx import Document
from transformers import pipeline

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file_path):
    with open(pdf_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Function to extract text from a DOCX (Word) file
def extract_text_from_docx(docx_file_path):
    doc = Document(docx_file_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to extract text from a TXT file
def extract_text_from_txt(txt_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Function to determine the file type and extract text accordingly
def extract_text_from_file(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported file format. Please upload a .pdf, .docx, or .txt file.")


# Load the pre-trained question-answering model
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")


# Function to get the answer from the document text based on the query
def get_answer_from_text(query, context):
    result = qa_pipeline(question=query, context=context)
    return result['answer']


# Main Logic
# Specify the file path in your local environment
file_path = input("Enter the full path to the document (PDF, DOCX, or TXT): ")

try:
    # Extract text from the file based on its format
    document_text = extract_text_from_file(file_path)
    print("\nDocument text extracted successfully.")
except ValueError as e:
    print(e)

# Input the query
query = input("\nEnter your query about the document: ")

# Get the answer from the text based on the query
answer = get_answer_from_text(query, document_text)

# Display the answer
print(f"\nAnswer to your query: {answer}")
