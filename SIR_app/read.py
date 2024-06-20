import os
import pythoncom
import win32com.client
from docx import Document



def read_doc_file(file_name):
    # Base directory for document storage
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(BASE_DIR, 'SIR_app/Data')
    doc_path = os.path.join(data_dir, file_name)  # Construct the full file path

    pythoncom.CoInitialize()  # Initialize the COM library

    try:
        if doc_path.endswith('.docx'):
            # For .docx files, use the python-docx library
            doc = Document(doc_path)
            paragraphs = [paragraph.text for paragraph in doc.paragraphs]
            return '\n'.join(paragraphs)
        elif doc_path.endswith('.doc'):
            # For .doc files, use the pywin32 library
            word_app = win32com.client.Dispatch('Word.Application')
            doc = word_app.Documents.Open(doc_path)
            content = doc.Content.Text
            doc.Close()
            return content
        else:
            print(f"Unsupported file format: {doc_path}")
            return None
    finally:
        pythoncom.CoUninitialize()  # Uninitialize the COM library

# Global dictionary to store documents' content
documents = {}

def read_documents():
    # List all files in the specific directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(BASE_DIR, 'SIR_app/Data')

    for file_name in os.listdir(data_dir):
        if file_name not in documents:  # Check if the file's content is already cached
            documents[file_name] = read_doc_file(file_name)

    return documents

# Initial call to populate the documents dictionary
document_contents = read_documents()
