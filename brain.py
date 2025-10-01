from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer
import ollama
from sentence_transformers import CrossEncoder


def ask(question: str, knowledge: str):
    load_dotenv()

    try:
        llm = ChatOllama(
            model = 'gemma3:4b',
            validate_model_on_init = True,
            temperature = os.getenv('TEMPERATURE'),
        )

        system_prompt = os.getenv('CHAT_PROMPT')
        system_prompt = system_prompt.replace('[CONHECIMENTO]', knowledge)

        messages = [
            ('system', system_prompt),
            ('human', question),
        ]

        for chunk in llm.stream(messages):
            yield chunk.content
    except Exception as e:
        print(f'Erro na resposta da IA: {e}')
        return 'Ops... Houve algum problema no meu processamento, não consigo te responder. Mas, tente novamente.'

def get_question_transformed(question: str) -> str:
    load_dotenv()
    
    try:
        system_prompt = os.getenv('TRANSFORM_PROMPT')
        system_prompt = system_prompt.replace('[QUESTION]', question)

        llm_client = ollama
        response = llm_client.generate(
            model='qwen3:8b',
            prompt=system_prompt
        )
        
        content = response['response']
        answer_idx = content.find('</think>') + len('</think>')
        content = content[answer_idx:len(content)]
        return content
        
    except Exception as e:
        print(f'Erro ao gerar documento hipotético HyDE: {e}')
        return f'''
            A resposta para "{question}" é:,
            Sobre {question}:,
            Em relação a {question}, podemos dizer que
        '''

def reclassification(question: str, docs: list[str]) -> list[str]:
    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    pairs = [(question, doc) for doc in docs]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

    return [doc for doc, score in ranked]

def embedding(text) -> list[float]:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(text).tolist()