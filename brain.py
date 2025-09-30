from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer
import ollama


def ask(question, knowledge):
    load_dotenv()

    try:
        llm = ChatOllama(
            model = 'gemma3:4b',
            validate_model_on_init = True,
            temperature = os.getenv('TEMPERATURE'),
        )

        system_prompt = os.getenv('CHAT_PROMPT')

        system_prompt += knowledge

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
    try:
        prompt = f'''Faça exatamente o que eu pedir.
Seja o mais breve e claro possível.
Transforme a pergunta para que ela seja mais específica possível: "{question}"'''

        llm_client = ollama
        response = llm_client.generate(
            model='gemma3:4b',
            prompt=prompt
        )
        
        content = response['response']
        # answer_idx = content.find('</think>') + len('</think>')
        # content = content[answer_idx:len(content)]
        return content
        
    except Exception as e:
        print(f'Erro ao gerar documento hipotético HyDE: {e}')
        return f'''
            A resposta para "{question}" é:,
            Sobre {question}:,
            Em relação a {question}, podemos dizer que
        '''

def embedding(text) -> list[float]:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(text).tolist()