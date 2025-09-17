from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer


def ask(question, knowledge):
    load_dotenv()

    llm = ChatOllama(
        model = "qwen3:4b",
        validate_model_on_init = True,
        temperature = os.getenv('TEMPERATURE'),
        # num_predict removido para usar o limite padrão do modelo
        # other params ...
    )

    system_prompt = os.getenv('SYSTEM_PROMPT')

    system_prompt += knowledge

    messages = [
        ("system", system_prompt),
        ("human", question),
    ]

    preparingAnswer = False
    initAnswer = False
    chunkContent = ''
    for chunk in llm.stream(messages):
        chunkContent += chunk.content
        if preparingAnswer:
            initAnswer = True
            preparingAnswer = False
        elif initAnswer:
            yield chunk.content
        elif '</think>' in chunkContent:
            preparingAnswer = True

def embedding(text) -> list[float]:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(text).tolist()