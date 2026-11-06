
from PyPDF2 import PdfReader
from pathlib import Path


def extract_resume_text(uploaded_file):
    """
    Extract text from an uploaded PDF resume.
    """

    try:
        reader = PdfReader(uploaded_file)

        extracted_text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text + "\n"

        return extracted_text.strip()

    except Exception as e:
        return f"Error reading PDF: {e}"


def extract_text_from_file(file_path):
    """
    Extract text from a PDF file path.
    """

    try:
        reader = PdfReader(str(file_path))

        extracted_text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text + "\n"

        return extracted_text.strip()

    except Exception as e:
        return f"Error reading PDF: {e}"


if __name__ == "__main__":
    print("Resume parser module is ready!")
