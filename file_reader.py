import pdfplumber
import os
from dotenv import load_dotenv


load_dotenv()
__max_chunk_chars = int(os.getenv('MAX_CHARS_PER_FILE_CHUNK'))

def read(file_name):
    with pdfplumber.open(file_name) as pdf:
        total_pages = len(pdf.pages)
        count = 0
        for page in pdf.pages:
            extracted_text = page.extract_text()

            count += 1
            percent = count * 100 / total_pages

            text_idx = 0
            done = False
            while not done:
                chunk = extracted_text[text_idx:text_idx + __max_chunk_chars]
                text_idx += __max_chunk_chars
                yield chunk, round(percent, 2)

                done = __max_chunk_chars >= len(extracted_text) or (text_idx + 1) >= len(extracted_text)
