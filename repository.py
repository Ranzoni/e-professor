import psycopg
from dotenv import load_dotenv
import os


class DatabaseConnectionError(Exception):
    """Exceção para erros de conexão com o banco de dados"""
    pass

class RepoConnection():
    def __init__(self):
        """Inicia uma instância do DbConnection"""
        self.__connection = None

    def __del__(self):
        """Método chamado quando o objeto é destruído"""
        self.disconnect()

    def connect(self):
        """Cria a conexão com o banco de dados"""

        load_dotenv()

        try:
            self.__connection = psycopg.connect(
                host=os.getenv('DATABASE_HOST'),
                port=os.getenv('DATABASE_PORT'),
                dbname=os.getenv('DATABASE_NAME'),
                user=os.getenv('DATABASE_USER'),
                password=os.getenv('DATABASE_PASS')
            )
        except Exception as e:
            raise DatabaseConnectionError(e)

    def disconnect(self):
        """Remove a conexão com o banco de dados"""

        if self.__connection:
            try:
                self.__connection.close()
            except Exception:
                pass

    def save_file(self, file_name: str) -> int:
        """Faz uma inserção do nome do arquivo no repositório"""

        connection = self.__get_connection()
        
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO files_read (file_name) 
                VALUES (%s)
                RETURNING id;
            """, (file_name,))
            
            file_id = cursor.fetchone()[0]

        return file_id

    def file_exists(self, file_name: str) -> bool:
        """Verifica se o nome do arquivo existe no repositório"""

        connection = self.__get_connection()
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(1) > 0 FROM files_read
                WHERE LOWER(file_name) = LOWER(%s);
            """, (file_name,))
            
            data = cursor.fetchone()

        return data[0] if data else False

    def save_embedding(self, embedding: list[float], content: str, file_id: int) -> int:
        """Salva o conteúdo e seu valor vetorial no repositório"""

        connection = self.__get_connection()
        
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO files_embedding (embedding, content, files_read_id) 
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (embedding, content, file_id))
            
            embedding_id = cursor.fetchone()[0]

        return embedding_id

    def commit(self):
        """Persiste todos os comandos de inserção/alteração/exclusão no repositório"""

        connection = self.__get_connection()
        connection.commit()

    def rollback(self):
        """Desfaz todos os comandos de inserção/alteração/exclusão no repositório"""

        connection = self.__get_connection()
        connection.rollback()

    def get_relevants_contents(self, embedding: list[float]) -> list[str]:
        """Faz uma busca semântica do texto no repositório"""

        connection = self.__get_connection()

        with connection.cursor() as cursor:
            max_contents = os.getenv('MAX_CONTENTS')
            semantic_distance = os.getenv('SEMANTIC_DISTANCE')

            cursor.execute("""
                WITH embeddings_ranked AS (
                    SELECT fe.content, fe.embedding <-> %s::vector AS distance 
                    FROM files_embedding fe 
                    ORDER BY distance 
                    LIMIT %s
                ) 
                SELECT content FROM embeddings_ranked 
                WHERE distance < %s 
                ORDER BY distance;
            """, (embedding, max_contents, semantic_distance))
            
            rows = cursor.fetchall()

        return [row[0] for row in rows] if rows else []

    def __get_connection(self) -> psycopg.Connection:
        if not self.__connection:
            raise DatabaseConnectionError("Conexão com o banco de dados não foi estabelecida. Chame connect() primeiro.")
        
        if self.__connection.closed:
            raise DatabaseConnectionError("Conexão com o banco foi fechada. Reconecte antes de usar.")
        
        return self.__connection
