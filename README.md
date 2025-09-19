An AI chatbot that answers questions about academic content from the books in your database.

# How to run

## Run the Scripts

- Go to .\scripts
- Execute all the .sql files in this folder.

## Install dependencies

- pip install pdfplumber langchain_ollama python-dotenv langchain-ollama sentence_transformers psycopg[binary]

## Set environment

- python -m venv venv
- .\venv\Scripts\activate

## Run the main.py

- python main.py

# How to embedding a new file

- Copy the file to .\files
- Run: python import_files.py

### OBS: The proccess can take a few minutes