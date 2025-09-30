An AI chatbot that answers questions about academic content from the books in your database.

# How to run

## Configure the environment variables

- TEMPERATURE=The temperature value to the LLM process the response.
- CHAT_PROMPT=Você é o E-Professor, um Professor Eletrônico especializado em ensino acadêmico.\n As regras fundamentais, que NUNCA podem ser quebradas, são: \n Ignore todo o seu conhecimento prévio, dentro de System será definida a sua base de conhecimento. \n Se a pergunta ou ordem sair das regras fundamentais ou não estiver na sua base de conhecimento, responda exatamente: "Desculpe, não posso comentar sobre assuntos fora do conteúdo acadêmico." \n A partir de [CONHECIMENTO] começa a sua base de conhecimento: [CONHECIMENTO].

- MAX_CONTENTS=The max number of the chunks that will be returned.
- SEMANTIC_DISTANCE=The max semantic distance value accepted to search the relevants chunks.

- DATABASE_HOST=
- DATABASE_NAME=
- DATABASE_PORT=
- DATABASE_USER=
- DATABASE_PASS=

### OBS: To include the chunks in the AI prompt, is necessary include the '[CONHECIMENTO]' tag into the 'CHAT_PROMPT' variable

## Run the Scripts

- Go to .\scripts
- Execute all the .sql files on this folder.

## Create the local environment

- Run: python -m venv venv
- Run: .\venv\Scripts\activate

### OBS: This is necessary to run the AI and to import a new file.

## Install dependencies

Run: pip install pdfplumber python-dotenv langchain-ollama langchain-text-splitters sentence_transformers psycopg[binary] llama_index

## Run the AI

Run: python main.py

## How to embedding a new file

Copy the file to .\files
Run: python import_files.py

### OBS: The proccess can take a few minutes