import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os


def read(file_name):
    with pdfplumber.open(file_name) as pdf:
        total_pages = len(pdf.pages)
        count = 0
        for page in pdf.pages:
            extracted_text = page.extract_text()

            count += 1
            percent = count * 100 / total_pages

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=int(os.getenv("CHUNK_SIZE", 512)),
                chunk_overlap=int(os.getenv("CHUNK_OVERLAP", 50))
            )

            chunks = splitter.split_text(extracted_text)
            for chunk in chunks:
                yield chunk, round(percent, 2)
