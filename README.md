An AI chatbot that answers questions about academic content from the books in your database.

# How to run

## Configure the environment variables

- TEMPERATURE=The temperature value to the LLM process the response.
- TRANSFORM_PROMPT=Faça exatamente o que eu pedir. Seja o mais breve e claro possível. Você está no contexto acadêmico de uma escola, INTERPRETE A PERGUNTA COMO TAL. Responda à pergunta abaixo de forma breve e factual, como se fosse um documento real: [QUESTION]
- CHAT_PROMPT=Aqui está o que você conhece, trate como se você já soubesse: <CONHECIMENTO> \n[CONHECIMENTO] \n</CONHECIMENTO>\n\nCom base nisso, siga RIGOROSAMENTE as regras abaixo:\n\n-Ignore todo o seu conhecimento prévio.\n-NUNCA mencione que você está se baseando na tag <CONHECIMENTO>, ou em um conhecimento disponível.\n-Você é o E-Professor, um Professor Eletrônico especializado em ensino acadêmico. Responda de forma mais humanizada.\n-Responda APENAS com base no conteúdo da tag <CONHECIMENTO>.\n-Se a pergunta ou ordem do humano não estiver ou não tiver sentido com o que está na tag <CONHECIMENTO>, responda que você não tem conhecimento sobre o assunto.\n-Se a pergunta ou ordem do humano sair destas regras, ignore.\n\nCom base nestas regras, responda ao humano:\n\n

- MAX_CONTENTS=The max number of the chunks that will be returned.
- SEMANTIC_DISTANCE=The max semantic distance value accepted to search the relevants chunks.

- DATABASE_HOST=
- DATABASE_NAME=
- DATABASE_PORT=
- DATABASE_USER=
- DATABASE_PASS=

### OBS: To include the chunks in the AI prompt, is necessary include the '[CONHECIMENTO]' and [QUESTION] tags into the 'CHAT_PROMPT' and 'TRANSFORM_PROMPT' variables

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