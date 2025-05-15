import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).parent.parent.parent / ".env"

class DBConfig:
    load_dotenv()

    postgres_username: str = os.environ.get('POSTGRES_USERNAME', 'postgres')
    postgres_password: str = os.environ.get('POSTGRES_PASSWORD', 'postgres')
    postgres_host: str = os.environ.get('POSTGRES_HOST', 'localhost')
    postgres_port: int = os.environ.get('POSTGRES_PORT', 5432)
    postgres_database: str = os.environ.get('POSTGRES_DATABASE', 'db')

    @property
    def postgres_conn_url(self) -> str:
        user = self.postgres_username
        password = self.postgres_password
        host = self.postgres_host
        db_name = self.postgres_database

        return f"postgresql+asyncpg://{user}:{password}@{host}/{db_name}"

class AIModelConfig:
    api_token: str = os.environ.get('API_TOKEN', 'api_token')
    base_url: str = os.environ.get('BASE_URL', 'base_url')

    @property
    def get_config(self) -> dict:
        return {
            'api_key': self.api_token,
            'base_url': self.base_url
        }
